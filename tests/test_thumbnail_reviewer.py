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
        if "<script>" not in cls.html or "</script>" not in cls.html:
            raise AssertionError("Thumbnail reviewer must contain its standalone JavaScript.")
        cls.script = cls.html.split("<script>", 1)[1].split("</script>", 1)[0]

    def test_reviewer_has_review_and_recovery_controls(self) -> None:
        required_ids = {
            "indexFile", "sessionFile", "loadIndex", "importSession", "exportSession",
            "metricEntries", "metricThumbs", "metricReviewed", "metricPending",
            "query", "category", "reviewFilter", "onlyThumbs", "recordList",
            "thumbImage", "openSource", "openThumbnail", "extraBox", "licenseText",
            "notes", "saveReview", "saveNext", "previous", "next",
        }
        ids = set(re.findall('id="([^"]+)"', self.html))
        self.assertTrue(required_ids.issubset(ids), f"Missing controls: {sorted(required_ids - ids)}")

    def test_reviewer_preserves_permissions_and_originals(self) -> None:
        self.assertIn("no se suben imágenes", self.html.lower())
        self.assertIn("nunca reescriben el índice maestro automáticamente", self.html)
        self.assertIn("thumbnail_correspondence_manual", self.script)
        self.assertIn("Misma URL de miniatura en", self.html)
        self.assertIn("veredicto visual", self.html.lower())

    def test_tool_has_no_external_script_or_framework_dependency(self) -> None:
        self.assertNotIn("<script src=", self.html.lower())
        self.assertNotIn("cdn.jsdelivr.net", self.html.lower())
        self.assertNotIn("unpkg.com", self.html.lower())
        self.assertNotIn("cdnjs.cloudflare.com", self.html.lower())

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
