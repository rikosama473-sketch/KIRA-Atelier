from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "tools" / "visual-reference-library" / "thumbnail-reviewer.html"


class ThumbnailReviewerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = APP.read_text(encoding="utf-8")
        match = re.search(r"<script>([\\s\\S]*?)</script>", cls.html)
        if not match:
            raise AssertionError("Thumbnail reviewer must contain its standalone JavaScript.")
        cls.script = match.group(1)

    def test_reviewer_has_review_and_recovery_controls(self) -> None:
        required_ids = {
            "indexFile", "sessionFile", "loadIndex", "importSession", "exportSession",
            "metricEntries", "metricThumbs", "metricReviewed", "metricPending",
            "query", "category", "reviewFilter", "onlyThumbs", "recordList",
            "thumbImage", "openSource", "openThumbnail", "extraBox", "licenseText",
            "notes", "saveReview", "saveNext", "previous", "next",
        }
        ids = set(re.findall(r'\\bid="([^"]+)"', self.html))
        self.assertTrue(required_ids.issubset(ids), f"Missing controls: {sorted(required_ids - ids)}")

    def test_reviewer_preserves_permissions_and_originals(self) -> None:
        self.assertIn("no se suben imágenes", self.html.lower())
        self.assertIn("never reescriben el índice maestro automáticamente", self.html)
        self.assertIn("thumbnail_correspondence_manual", self.script)
        self.assertIn("URL repetida en el censo", self.html)
        self.assertIn("veredictos", self.html.lower())

    def test_tool_has_no_external_script_or_framework_dependency(self) -> None:
        self.assertNotRegex(self.html, r'<script[^>]+src=')
        self.assertNotRegex(self.html, r'https://(?:cdn\\.|unpkg\\.|cdnjs\\.)')

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_inline_javascript_syntax(self) -> None:
        with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as handle:
            handle.write(self.script)
            path = Path(handle.name)
        try:
            result = subprocess.run(
                ["node", "--check", str(path)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
        finally:
            path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
