import importlib.util
import json
import re
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "select_next_character_asset_task.py"
SPEC = importlib.util.spec_from_file_location("character_asset_queue", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

FACTORY_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "generate_character_assets_free.py"
FACTORY_SPEC = importlib.util.spec_from_file_location("character_asset_factory_for_queue", FACTORY_SCRIPT)
FACTORY_MODULE = importlib.util.module_from_spec(FACTORY_SPEC)
FACTORY_SPEC.loader.exec_module(FACTORY_MODULE)


class CharacterAssetQueueTests(unittest.TestCase):
    def make_root(self, temp):
        root = Path(temp)
        (root / "data").mkdir()
        (root / "from-PixAI-2034984086876227343-0.png").write_bytes(b"pibara-source")
        registry = {
            "characters": [
                {"id": "pibara", "source_images": ["from-PixAI-2034984086876227343-0.png"]},
                {"id": "sunna", "source_images": []},
                {"id": "chie", "source_images": []},
            ]
        }
        (root / "data" / "character-prompt-registry.json").write_text(
            json.dumps(registry), encoding="utf-8"
        )
        return root

    def mark_complete(self, root, pack, character="pibara", reference="from-PixAI-2034984086876227343-0.png"):
        source = root / reference
        sha = MODULE.source_sha256(source)
        run_dir = root / "generated" / "character-assets" / character / ("run-" + pack)
        render_dir = run_dir / "renders"
        render_dir.mkdir(parents=True, exist_ok=True)
        slug = {
            "anatomy-sheet-4": "batch-front-a-pose",
            "anatomy-guide-1": "full-body-anatomy-a-pose",
            "anatomy-front-v2-1": "full-body-front-a-pose-v2",
            "anatomy-side-1": "full-body-side-profile",
            "anatomy-back-1": "full-body-back-view",
            "anatomy-joint-guide-1": "full-body-joint-guide",
            "hair-core-5": "blunt-bob",
            "expressions-core-5": "happy",
            "eyes-4": "eye-catchlights",
            "accessories-4": "ribbon",
            "face-details-4": "freckles",
        }[pack]
        render = render_dir / f"{slug}.png"
        render.write_bytes(b"png-placeholder-for-queue-test")
        manifest = {
            "character_id": character,
            "pack": pack,
            "pack_status": "complete",
            "source": {"path": reference, "sha256": sha},
            "required_asset_ids": [slug],
            "completed_asset_ids": [slug],
            "variants": [{"asset_id": slug, "render": {"file": render.relative_to(root).as_posix()}}],
        }
        (run_dir / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")



    def test_workflow_dispatch_validation_and_queue_match_generator_packs(self):
        workflow_path = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "generate-character-assets-free.yml"
        workflow = workflow_path.read_text(encoding="utf-8")

        input_start = workflow.index("      asset_pack:")
        input_end = workflow.index("      background:", input_start)
        asset_pack_input = workflow[input_start:input_end]
        self.assertIn("        options:\n", asset_pack_input)
        options_text = asset_pack_input.split("        options:\n", 1)[1]
        dispatch_packs = set(re.findall(r"^\s+- ([a-z0-9-]+)\s*$", options_text, re.MULTILINE))

        guard_start = workflow.index("          supported_packs = {")
        guard_end = workflow.index("          }", guard_start)
        validation_packs = set(re.findall(r'"([a-z0-9-]+)"', workflow[guard_start:guard_end]))

        generator_packs = set(FACTORY_MODULE.PACKS)
        self.assertEqual(set(MODULE.PACK_ORDER), generator_packs)
        self.assertEqual(dispatch_packs, generator_packs)
        self.assertEqual(validation_packs, generator_packs)
        self.assertIn("anatomy-back-1", dispatch_packs)

    def test_workflow_checks_out_and_commits_generated_image_library(self):
        workflow_path = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "generate-character-assets-free.yml"
        workflow = workflow_path.read_text(encoding="utf-8")

        checkout_start = workflow.index("          sparse-checkout: |")
        checkout_end = workflow.index("          sparse-checkout-cone-mode: true", checkout_start)
        checkout_rules = workflow[checkout_start:checkout_end]
        self.assertIn("            tools/avatar-maker/assets", checkout_rules)

        commit_start = workflow.index("      - name: Commit generated assets and resumable progress to main")
        commit_step = workflow[commit_start:]
        self.assertIn("          git add -A -- tools/avatar-maker/assets/image-library.json", commit_step)

    def test_starts_with_first_incomplete_pibara_pack(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.make_root(temp)
            task = MODULE.select_next_task(root)
            self.assertEqual(task["character_id"], "pibara")
            self.assertEqual(task["asset_pack"], "anatomy-sheet-4")
            self.assertEqual(task["reference_image"], "from-PixAI-2034984086876227343-0.png")

    def test_moves_to_next_pack_when_anatomy_batch_is_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.make_root(temp)
            self.mark_complete(root, "anatomy-sheet-4")
            task = MODULE.select_next_task(root)
            self.assertEqual(task["asset_pack"], "anatomy-guide-1")

    def test_moves_to_sunna_only_when_a_reference_is_registered(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.make_root(temp)
            for pack in MODULE.PACK_ORDER:
                self.mark_complete(root, pack)
            (root / "sunna-reference.png").write_bytes(b"sunna-source")
            registry_path = root / "data" / "character-prompt-registry.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["characters"][1]["source_images"] = ["sunna-reference.png"]
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            task = MODULE.select_next_task(root)
            self.assertEqual(task["character_id"], "sunna")
            self.assertEqual(task["reference_image"], "sunna-reference.png")

    def test_never_reuses_pibara_reference_for_chie_or_sunna(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.make_root(temp)
            for pack in MODULE.PACK_ORDER:
                self.mark_complete(root, pack)
            registry_path = root / "data" / "character-prompt-registry.json"
            registry = json.loads(registry_path.read_text(encoding="utf-8"))
            registry["characters"][1]["source_images"] = ["from-PixAI-2034984086876227343-0.png"]
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            self.assertIsNone(MODULE.select_next_task(root))

    def test_returns_none_when_no_confirmed_references_remain(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.make_root(temp)
            for pack in MODULE.PACK_ORDER:
                self.mark_complete(root, pack)
            self.assertIsNone(MODULE.select_next_task(root))


    def test_partial_manifest_does_not_mark_pack_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.make_root(temp)
            self.mark_complete(root, "anatomy-sheet-4")
            self.mark_complete(root, "anatomy-guide-1")
            manifest_path = next(
                (root / "generated" / "character-assets" / "pibara").rglob("manifest.json")
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["pack_status"] = "partial"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            task = MODULE.select_next_task(root)
            self.assertEqual(task["asset_pack"], "anatomy-guide-1")

    def test_missing_render_file_does_not_mark_pack_complete(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.make_root(temp)
            self.mark_complete(root, "anatomy-sheet-4")
            self.mark_complete(root, "anatomy-guide-1")
            manifest_path = next(
                path for path in (root / "generated" / "character-assets" / "pibara").rglob("manifest.json")
                if json.loads(path.read_text(encoding="utf-8"))["pack"] == "anatomy-guide-1"
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            render_path = root / manifest["variants"][0]["render"]["file"]
            render_path.unlink()
            task = MODULE.select_next_task(root)
            self.assertEqual(task["asset_pack"], "anatomy-guide-1")

    def test_changed_source_reference_invalidates_old_completed_manifests(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.make_root(temp)
            self.mark_complete(root, "anatomy-sheet-4")
            source = root / "from-PixAI-2034984086876227343-0.png"
            source.write_bytes(b"updated-pibara-source")
            task = MODULE.select_next_task(root)
            self.assertEqual(task["asset_pack"], "anatomy-sheet-4")


if __name__ == "__main__":
    unittest.main()
