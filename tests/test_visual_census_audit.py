from __future__ import annotations

import json
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


if __name__ == "__main__":
    unittest.main()
