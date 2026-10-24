from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "tools" / "design-mixer" / "index.html"
MODULE_README = ROOT / "tools" / "design-mixer" / "README.md"
PROJECT_README = ROOT / "README.md"


class DesignMixerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = APP.read_text(encoding="utf-8")
        cls.module_readme = MODULE_README.read_text(encoding="utf-8")
        cls.project_readme = PROJECT_README.read_text(encoding="utf-8")
        match = re.search(r"<script>([\s\S]*?)</script>", cls.html)
        if not match:
            raise AssertionError("Design Mixer must contain its standalone JavaScript.")
        cls.script = match.group(1)

    def test_required_workflow_controls_exist(self) -> None:
        required_ids = {
            "fileInput",
            "folderInput",
            "projectInput",
            "gallery",
            "searchInput",
            "cropCanvas",
            "categorySelect",
            "pieceNote",
            "partList",
            "boardCanvas",
            "exportBoard",
            "saveProject",
            "makePrompt",
            "promptOutput",
        }
        actual_ids = set(re.findall(r'\bid="([^"]+)"', self.html))
        self.assertTrue(required_ids.issubset(actual_ids), sorted(required_ids - actual_ids))

    def test_dom_ids_are_unique_and_script_targets_exist(self) -> None:
        ids = re.findall(r'\bid="([^"]+)"', self.html)
        duplicates = sorted({item for item in ids if ids.count(item) > 1})
        self.assertEqual([], duplicates, f"Duplicate HTML IDs: {duplicates}")
        referenced = set(re.findall(r'document\.getElementById\("([^"]+)"\)', self.script))
        self.assertTrue(referenced.issubset(set(ids)), sorted(referenced - set(ids)))

    def test_module_has_no_remote_script_or_stylesheet_dependencies(self) -> None:
        self.assertNotRegex(self.html, r"<script[^>]+src\s*=")
        self.assertNotRegex(self.html, r'<link[^>]+href=["\']https?://')
        self.assertIn("Las imágenes se leen directamente", self.module_readme)
        self.assertIn("no tiene una función de subida", self.module_readme)

    def test_exports_and_readme_entry_are_documented(self) -> None:
        for phrase in ("kira-tablero-inspiracion.png", "kira-prompt-diseno.txt", "kira-design-mixer-project.json"):
            self.assertIn(phrase, self.html)
        self.assertIn("tools/design-mixer/index.html", self.project_readme)
        self.assertIn("segmentación automática", self.module_readme.lower())

    def test_embedded_javascript_parses_when_node_is_available(self) -> None:
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js is not installed in this environment.")
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as temp:
            temp.write(self.script)
            temp_path = Path(temp.name)
        try:
            result = subprocess.run(
                [node, "--check", str(temp_path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, result.returncode, result.stderr or result.stdout)
        finally:
            temp_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
