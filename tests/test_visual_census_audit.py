from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import audit_visual_census  # noqa: E402


class VisualCensusAuditTests(unittest.TestCase):
    def _write_fixture(self, directory: Path, rows: list[dict]) -> tuple[Path, Path]:
        json_path = directory / "index.json"
        html_path = directory / "atlas.html"
        json_path.write_text(json.dumps({"project": "KIRA Atelier", "reference_entries": rows}), encoding="utf-8")
        html_path.write_text("<script>const records=" + json.dumps(rows) + ";</script>", encoding="utf-8")
        return json_path, html_path

    def _row(self, identifier: str, source: str, **extra: object) -> dict:
        row = {
            "id": identifier,
            "title": identifier,
            "source_url": source,
            "url": source,
            "thumbnail_url": None,
            "red_warning_required": False,
            "license_status": "not_independently_verified_by_indexer",
        }
        row.update(extra)
        return row

    def test_current_atlas_is_structurally_consistent(self) -> None:
        report = audit_visual_census.audit_documents()
        self.assertTrue(report["ok"], "\n".join(report["errors"]))
        self.assertEqual(report["stats"]["json_entries"], report["stats"]["html_entries"])
        self.assertTrue(report["stats"]["json_html_ids_match_in_order"])
        self.assertTrue(report["stats"]["json_html_key_fields_match"])
        self.assertEqual(report["stats"]["red_warning_gaps"], 0)
        self.assertGreaterEqual(report["stats"]["json_entries"], 340)

    def test_page_cover_visual_check_pending_is_counted_but_confirmed_thumb_is_not(self) -> None:
        report = audit_visual_census.audit_documents()
        self.assertTrue(report["ok"], "\\n".join(report["errors"]))
        pending_ids = {
            row["id"]
            for row in report["issues"]["thumbnail_status_unverified_or_unknown"]
        }
        self.assertTrue(
            {"CENSUS-A-13", "CENSUS-A-15", "CENSUS-A-17", "CENSUS-A-20"} <= pending_ids
        )
        self.assertTrue(
            {"EXT-ITCH-009", "EXT-TOOL-001", "EXT-BOOTH-003"} <= pending_ids
        )
        self.assertIn("EXT-TOOL-004", pending_ids, "Spanish pending statuses must also be counted.")
        self.assertTrue(
            {"EXT-ITCH-010", "EXT-ITCH-011", "EXT-TOOL-002", "EXT-HIR-015"}.isdisjoint(pending_ids)
        )

    def test_license_review_claims_and_scope_uncertainty_are_counted(self) -> None:
        report = audit_visual_census.audit_documents()
        self.assertTrue(report["ok"], "\\n".join(report["errors"]))
        pending_ids = set(report["issues"]["records_with_unverified_or_missing_license_status"])
        self.assertTrue(
            {"CENSUS-C-03", "CENSUS-A-04", "EXT-ITCH-010", "EXT-ITCH-011", "EXT-TOOL-001"} <= pending_ids
        )

    def test_atlas_cards_expose_thumbnail_and_asset_use_status(self) -> None:
        atlas_path = ROOT / "trabajo aparte" / "censo-visual-interactivo.html"
        html = atlas_path.read_text(encoding="utf-8")
        self.assertIn("function thumbnailReviewText(e)", html)
        self.assertIn("function assetUseText(e)", html)
        self.assertIn('class="verify-status"', html)
        self.assertIn('class="asset-use"', html)
        self.assertIn("e.thumbnail_status", html)
        self.assertIn("e.asset_use_recommendation", html)
        self.assertIn("return asText(e.asset_use_recommendation);", html)

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_atlas_inline_javascript_syntax(self) -> None:
        atlas_path = ROOT / "trabajo aparte" / "censo-visual-interactivo.html"
        html = atlas_path.read_text(encoding="utf-8")
        self.assertIn("<script>", html)
        self.assertIn("</script>", html)
        script = html.split("<script>", 1)[1].split("</script>", 1)[0]
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
            handle.write(script)
            script_path = Path(handle.name)
        try:
            result = subprocess.run(
                ["node", "--check", str(script_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
        finally:
            script_path.unlink(missing_ok=True)

    def test_parser_respects_brackets_and_escaped_quotes_inside_strings(self) -> None:
        html = r'''<script>const records=[{"id":"x","source_url":"https://example.test/a?x=[1]","title":"a \"quoted\" title"}];</script>'''
        rows = audit_visual_census.parse_html_records(html)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["id"], "x")
        self.assertIn("[1]", rows[0]["source_url"])

    def test_duplicate_source_url_is_a_structural_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rows = [
                self._row("one", "https://example.test/source"),
                self._row("two", "https://example.test/source"),
            ]
            json_path, html_path = self._write_fixture(Path(tmp), rows)
            report = audit_visual_census.audit_documents(json_path, html_path)
            self.assertFalse(report["ok"])
            self.assertIn("duplicate_source_urls_json", report["issues"])
            self.assertTrue(any("duplicate canonical source URLs" in item for item in report["errors"]))

    def test_missing_red_warning_flag_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            rows = [
                self._row(
                    "one",
                    "https://example.test/source",
                    extras_red="Unrelated face and costume",
                    red_warning_required=False,
                )
            ]
            json_path, html_path = self._write_fixture(Path(tmp), rows)
            report = audit_visual_census.audit_documents(json_path, html_path)
            self.assertFalse(report["ok"])
            self.assertEqual(report["stats"]["red_warning_gaps"], 1)

    def test_same_thumbnail_url_is_a_review_warning_not_auto_deletion(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            shared_thumb = "https://example.test/preview.jpg"
            rows = [
                self._row("one", "https://example.test/source-one", thumbnail_url=shared_thumb),
                self._row("two", "https://example.test/source-two", thumbnail_url=shared_thumb),
            ]
            json_path, html_path = self._write_fixture(Path(tmp), rows)
            report = audit_visual_census.audit_documents(json_path, html_path)
            self.assertTrue(report["ok"], "\n".join(report["errors"]))
            self.assertEqual(report["stats"]["shared_thumbnail_url_groups"], 1)
            self.assertEqual(len(report["issues"]["shared_thumbnail_url_groups"][0]["ids"]), 2)


    def test_duplicate_comparator_supports_distinct_pair_verdicts_and_safe_export(self) -> None:
        tool_path = ROOT / "tools" / "visual-reference-library" / "duplicate-comparator.html"
        self.assertTrue(tool_path.exists(), "The side-by-side duplicate comparator must be present.")
        html = tool_path.read_text(encoding="utf-8")
        for token in [
            'id="imageA"', 'id="imageB"',
            'data-decision="same_artwork"',
            'data-decision="same_work_variant"',
            'data-decision="similar_style_distinct"',
            'data-decision="different_artwork"',
            'reviewed_pairs',
            'normalized_thumbnail_url_candidate_pairs',
            'ni concede derechos de uso',
        ]:
            self.assertIn(token, html)
        self.assertIn("no modifica el índice", html.lower())
        self.assertIn("No se fusionan registros de forma automática", html)
        # Candidate matching is intentionally conservative: preserve the path case and query string.
        self.assertIn("parsed.origin.toLowerCase()+parsed.pathname+parsed.search", html)
        self.assertNotIn("decodeURI(parsed.pathname).replace", html)

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_duplicate_comparator_inline_javascript_syntax(self) -> None:
        tool_path = ROOT / "tools" / "visual-reference-library" / "duplicate-comparator.html"
        html = tool_path.read_text(encoding="utf-8")
        self.assertIn("<script>", html)
        self.assertIn("</script>", html)
        script = html.split("<script>", 1)[1].split("</script>", 1)[0]
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
            handle.write(script)
            script_path = Path(handle.name)
        try:
            result = subprocess.run(
                ["node", "--check", str(script_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
        finally:
            script_path.unlink(missing_ok=True)

    def test_october_modular_sources_preserve_rights_and_thumbnail_uncertainty(self) -> None:
        index_path = ROOT / "trabajo aparte" / "indice-visual-componentes.json"
        atlas_path = ROOT / "trabajo aparte" / "censo-visual-interactivo.html"
        parsed = json.loads(index_path.read_text(encoding="utf-8"))
        index_rows = {row["id"]: row for row in parsed["reference_entries"]}
        atlas_rows = {row["id"]: row for row in audit_visual_census.parse_html_records(
            atlas_path.read_text(encoding="utf-8")
        )}
        expected = {"EXT-BOOTH-011", "EXT-ITCH-012", "EXT-OGA-002", "EXT-BOOTH-012", "EXT-BOOTH-013"}
        self.assertTrue(expected <= index_rows.keys())
        self.assertTrue(expected <= atlas_rows.keys())
        for identifier in expected:
            for field in ("source_url", "thumbnail_url", "thumbnail_status", "license_status", "extras_red", "monochrome_plate_status"):
                self.assertEqual(index_rows[identifier].get(field), atlas_rows[identifier].get(field), (identifier, field))
            self.assertTrue(index_rows[identifier]["red_warning_required"])
            self.assertTrue(index_rows[identifier]["extras_red"])

        booth = index_rows["EXT-BOOTH-011"]
        self.assertIn("redistribution_prohibited", booth["license_status"])
        self.assertIn("No empaquetar", booth["asset_use_recommendation"])
        self.assertIn("Visual match confirmed", booth["thumbnail_status"])

        itch = index_rows["EXT-ITCH-012"]
        self.assertIn("CC0_1.0", itch["license_status"])
        self.assertIn("pending", itch["source_verification_level"].lower())
        self.assertIsNotNone(itch["thumbnail_url"])
        self.assertIn("pendiente", itch["thumbnail_status"].lower())

        oga = index_rows["EXT-OGA-002"]
        self.assertIsNone(oga["thumbnail_url"])
        self.assertEqual(oga["thumbnail_kind"], "no_source_specific_preview_available")
        self.assertIn("CC0_1.0", oga["license_status"])
        self.assertIn("no muestra", oga["thumbnail_status"].lower())

        aether = index_rows["EXT-BOOTH-012"]
        self.assertIn("source_texture_redistribution_prohibited", aether["license_status"])
        self.assertIn("Inspección visual completada", aether["thumbnail_status"])
        self.assertIn("Solo referencia de arquitectura", aether["asset_use_recommendation"])
        self.assertIn("NOT CONFIRMED", aether["monochrome_plate_status"])

        ruliyna = index_rows["EXT-BOOTH-013"]
        self.assertIn("texture_redistribution_prohibited", ruliyna["license_status"])
        self.assertIn("SAMPLE", ruliyna["thumbnail_status"])
        self.assertIn("No redistribuir", ruliyna["asset_use_recommendation"])
        self.assertIn("NOT CONFIRMED", ruliyna["monochrome_plate_status"])

    def test_atlas_header_counts_and_navigation_stay_current(self) -> None:
        atlas_path = ROOT / "trabajo aparte" / "censo-visual-interactivo.html"
        reviewer_path = ROOT / "tools" / "visual-reference-library" / "thumbnail-reviewer.html"
        index_path = ROOT / "trabajo aparte" / "indice-visual-componentes.json"
        atlas = atlas_path.read_text(encoding="utf-8")
        reviewer = reviewer_path.read_text(encoding="utf-8")
        index = json.loads(index_path.read_text(encoding="utf-8"))
        records = audit_visual_census.parse_html_records(atlas)
        self.assertEqual(len(records), len(index["reference_entries"]))
        self.assertIn(f"<strong>{len(records)}</strong>registros indexados", atlas)
        self.assertIn(f'<strong>{sum(bool(row.get("thumbnail_url")) for row in records)}</strong>URLs de vista previa registradas', atlas)
        self.assertIn("../tools/visual-reference-library/duplicate-comparator.html", atlas)
        self.assertIn('href="./duplicate-comparator.html">Comparar duplicados ↗', reviewer)

    def test_shared_thumbnail_candidate_keeps_both_records_and_restricts_asset_use(self) -> None:
        index_path = ROOT / "trabajo aparte" / "indice-visual-componentes.json"
        atlas_path = ROOT / "trabajo aparte" / "censo-visual-interactivo.html"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        rows = index["reference_entries"]
        html_rows = audit_visual_census.parse_html_records(atlas_path.read_text(encoding="utf-8"))
        ids = {"ACC-CENSUS-F2", "ACC-CENSUS-F3"}
        indexed = {row["id"]: row for row in rows if row.get("id") in ids}
        rendered = {row["id"]: row for row in html_rows if row.get("id") in ids}
        self.assertEqual(set(indexed), ids)
        self.assertEqual(set(rendered), ids)
        self.assertEqual(len({row["source_url"] for row in indexed.values()}), 2)
        self.assertEqual(len({row["thumbnail_url"] for row in indexed.values()}), 1)
        for record_id, row in indexed.items():
            peer_ids = ids - {record_id}
            self.assertEqual(row["thumbnail_duplicate_group_id"], "THUMB-SHARED-001")
            self.assertEqual(row["thumbnail_duplicate_review_status"], "candidate_pending_visual_comparison")
            self.assertTrue(any(peer in row["thumbnail_status"] for peer in peer_ids))
            self.assertTrue(row["red_warning_required"])
            self.assertIn("do not treat it as a distinct source-specific artwork", row["extras_red"])
            self.assertEqual(row["license_status"], "reference_only_source_artwork_reuse_not_verified")
            self.assertIn("without explicit permission", row["asset_use_recommendation"])
            self.assertEqual(row["rights_evidence_url"], "https://idrawfashion.com/terms-of-service/")
            for key in (
                "thumbnail_status", "thumbnail_duplicate_group_id",
                "thumbnail_duplicate_review_status", "thumbnail_duplicate_peer_ids",
                "license_status", "asset_use_recommendation", "rights_evidence_url",
                "extras_red", "red_warning_required",
            ):
                self.assertEqual(rendered[record_id].get(key), row.get(key), f"{record_id}: {key}")

if __name__ == "__main__":
    unittest.main()
