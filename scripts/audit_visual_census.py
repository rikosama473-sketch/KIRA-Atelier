#!/usr/bin/env python3
"""Validate the KIRA Atlas visual census without network access or image downloads.

The audit checks JSON/HTML consistency and flags review gaps. It does not establish
that a remote thumbnail loads, depicts the intended work, or grants reuse rights.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_JSON = ROOT / "trabajo aparte" / "indice-visual-componentes.json"
DEFAULT_HTML = ROOT / "trabajo aparte" / "censo-visual-interactivo.html"
UNVERIFIED_THUMBNAIL_TERMS = (
    "not yet verified",
    "not yet been verified",
    "not yet been visually verified",
    "visual verification remains pending",
    "not yet confirmed",
    "not visually checked",
    "not visually verified",
    "not independently loaded",
    "not independently obtained",
    "not loaded",
    "not rendered",
    "direct image rendering failed",
    "blocked",
    "failed",
    "pending",
    "not verified",
    "unverified",
    "not retrieved",
    "candidate",
    "metadata",
)
UNVERIFIED_LICENSE_TERMS = (
    "unverified",
    "pending",
    "unknown",
    "not verified",
    "not independently",
    "not stated",
    "requires_original_page_review",
    "scope_requires_verification",
    "scope_unresolved",
    "vary_by_pack",
    "check_included_third_party_dependencies",
)


def parse_html_records(html_text: str) -> list[dict[str, Any]]:
    """Extract the JSON-compatible const records=[...] payload from the atlas HTML."""
    match = re.search(r"\bconst\s+records\s*=\s*", html_text)
    if not match:
        raise ValueError("Could not find the const records=[...] array in the atlas HTML.")

    start = html_text.find("[", match.end())
    if start < 0:
        raise ValueError("The records assignment has no opening '['.")

    depth = 0
    in_string = False
    escaped = False
    end = -1
    for index in range(start, len(html_text)):
        char = html_text[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
            if depth == 0:
                end = index + 1
                break

    if end < 0:
        raise ValueError("The records array has unbalanced brackets.")
    value = json.loads(html_text[start:end])
    if not isinstance(value, list) or any(not isinstance(row, dict) for row in value):
        raise ValueError("The records assignment must contain a JSON array of objects.")
    return value


def source_url(row: dict[str, Any]) -> str:
    return str(row.get("source_url") or row.get("url") or "").strip()


def has_red_extra(row: dict[str, Any]) -> bool:
    values = [row.get("extras_red"), row.get("irrelevant_elements_red")]
    metadata = row.get("census_metadata")
    if isinstance(metadata, list):
        values.extend(
            item.get("irrelevant_elements_red")
            for item in metadata
            if isinstance(item, dict)
        )
    return any(str(value or "").strip() for value in values)


def _duplicate_groups(values: list[str]) -> list[dict[str, Any]]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for index, value in enumerate(values):
        if value:
            grouped[value].append(index)
    return [
        {"value": value, "positions": positions, "count": len(positions)}
        for value, positions in grouped.items()
        if len(positions) > 1
    ]


def _license_pending(status: Any) -> bool:
    value = str(status or "").strip().lower()
    return not value or any(term in value for term in UNVERIFIED_LICENSE_TERMS)


def audit_documents(
    json_path: str | Path = DEFAULT_JSON,
    html_path: str | Path = DEFAULT_HTML,
) -> dict[str, Any]:
    """Audit the consolidated JSON index and interactive HTML atlas."""
    report: dict[str, Any] = {
        "schema_version": "1.0.0",
        "checked_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "project": "KIRA Atelier",
        "ok": False,
        "errors": [],
        "warnings": [],
        "stats": {},
        "issues": {},
        "limitations": [
            "No network requests are made and no remote thumbnail is fetched.",
            "A recorded thumbnail URL does not prove visual correspondence with the source artwork.",
            "Matching URLs can reveal direct reuse, but different URLs can still show the same artwork.",
            "License labels are reported as metadata; this audit does not grant or infer reuse permission.",
        ],
    }

    try:
        parsed = json.loads(Path(json_path).read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        report["errors"].append(f"Cannot read valid JSON index: {exc}")
        return report

    if not isinstance(parsed, dict) or not isinstance(parsed.get("reference_entries"), list):
        report["errors"].append("JSON index must contain a reference_entries array.")
        return report
    json_rows = parsed["reference_entries"]
    if any(not isinstance(row, dict) for row in json_rows):
        report["errors"].append("Every JSON reference entry must be an object.")
        return report

    try:
        html_rows = parse_html_records(Path(html_path).read_text(encoding="utf-8-sig"))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report["errors"].append(f"Cannot parse the HTML atlas records: {exc}")
        return report

    json_ids = [str(row.get("id") or "").strip() for row in json_rows]
    html_ids = [str(row.get("id") or "").strip() for row in html_rows]
    json_sources = [source_url(row) for row in json_rows]
    html_sources = [source_url(row) for row in html_rows]
    json_thumbnails = [str(row.get("thumbnail_url") or "").strip() for row in json_rows]
    html_thumbnails = [str(row.get("thumbnail_url") or "").strip() for row in html_rows]

    json_duplicate_ids = _duplicate_groups(json_ids)
    html_duplicate_ids = _duplicate_groups(html_ids)
    json_duplicate_sources = _duplicate_groups(json_sources)
    invalid_ids = [
        {"position": index, "url": json_sources[index]}
        for index, identifier in enumerate(json_ids)
        if not identifier
    ]
    invalid_sources = [
        {"id": json_ids[index], "url": value}
        for index, value in enumerate(json_sources)
        if not value or urlparse(value).scheme not in {"http", "https"} or not urlparse(value).netloc
    ]

    html_by_id = {row.get("id"): row for row in html_rows}
    field_mismatches: list[dict[str, str]] = []
    for row in json_rows:
        row_id = row.get("id")
        other = html_by_id.get(row_id)
        if other is None:
            field_mismatches.append({"id": str(row_id), "field": "missing_in_html"})
            continue
        comparable = {
            "source_url": (source_url(row), source_url(other)),
            "thumbnail_url": (
                str(row.get("thumbnail_url") or ""),
                str(other.get("thumbnail_url") or ""),
            ),
            "red_warning_required": (
                str(bool(row.get("red_warning_required"))),
                str(bool(other.get("red_warning_required"))),
            ),
        }
        for field, (left, right) in comparable.items():
            if left != right:
                field_mismatches.append({"id": str(row_id), "field": field})

    red_warning_gaps = [
        {"id": str(row.get("id") or ""), "title": str(row.get("title") or "")}
        for row in json_rows
        if has_red_extra(row) and row.get("red_warning_required") is not True
    ]
    no_thumbnail = [
        {"id": str(row.get("id") or ""), "title": str(row.get("title") or "")}
        for row in json_rows
        if not str(row.get("thumbnail_url") or "").strip()
    ]
    unverified_thumbnails = [
        {"id": str(row.get("id") or ""), "status": str(row.get("thumbnail_status") or "")}
        for row in json_rows
        if str(row.get("thumbnail_url") or "").strip()
        and (
            not str(row.get("thumbnail_status") or "").strip()
            or any(
                term in str(row.get("thumbnail_status") or "").lower()
                for term in UNVERIFIED_THUMBNAIL_TERMS
            )
        )
    ]
    missing_license_status = [
        str(row.get("id") or "")
        for row in json_rows
        if not str(row.get("license_status") or "").strip()
    ]
    unverified_license_status = [
        str(row.get("id") or "")
        for row in json_rows
        if _license_pending(row.get("license_status"))
    ]

    grouped_thumbnails: dict[str, list[str]] = defaultdict(list)
    for row in json_rows:
        thumb = str(row.get("thumbnail_url") or "").strip()
        if thumb:
            grouped_thumbnails[thumb].append(str(row.get("id") or ""))
    duplicate_thumbnail_groups = [
        {"thumbnail_url": thumb, "ids": ids, "count": len(ids)}
        for thumb, ids in grouped_thumbnails.items()
        if len(ids) > 1
    ]

    license_counts = Counter(
        str(row.get("license_status") or "(missing)").strip() or "(missing)"
        for row in json_rows
    )
    json_id_set, html_id_set = set(json_ids), set(html_ids)
    ids_match = json_ids == html_ids
    fields_match = len(json_rows) == len(html_rows) and not field_mismatches

    report["stats"] = {
        "json_entries": len(json_rows),
        "html_entries": len(html_rows),
        "json_unique_ids": len(json_id_set),
        "html_unique_ids": len(html_id_set),
        "json_unique_source_urls": len({value for value in json_sources if value}),
        "html_unique_source_urls": len({value for value in html_sources if value}),
        "thumbnail_urls_recorded": sum(bool(value) for value in json_thumbnails),
        "unique_thumbnail_urls": len({value for value in json_thumbnails if value}),
        "records_without_thumbnail": len(no_thumbnail),
        "thumbnail_status_unverified_or_unknown": len(unverified_thumbnails),
        "records_with_unverified_or_missing_license_status": len(unverified_license_status),
        "records_missing_license_status_field": len(missing_license_status),
        "red_warning_gaps": len(red_warning_gaps),
        "shared_thumbnail_url_groups": len(duplicate_thumbnail_groups),
        "license_status_distribution": dict(sorted(license_counts.items())),
        "json_html_ids_match_in_order": ids_match,
        "json_html_key_fields_match": fields_match,
    }
    report["issues"] = {
        "missing_ids_json": invalid_ids,
        "duplicate_ids_json": json_duplicate_ids,
        "duplicate_ids_html": html_duplicate_ids,
        "duplicate_source_urls_json": json_duplicate_sources,
        "invalid_or_missing_source_urls": invalid_sources,
        "json_html_field_mismatches": field_mismatches,
        "red_warning_gaps": red_warning_gaps,
        "records_without_thumbnail": no_thumbnail,
        "thumbnail_status_unverified_or_unknown": unverified_thumbnails,
        "records_missing_license_status_field": missing_license_status,
        "records_with_unverified_or_missing_license_status": unverified_license_status,
        "shared_thumbnail_url_groups": duplicate_thumbnail_groups,
    }

    if invalid_ids:
        report["errors"].append("One or more JSON entries have a missing ID.")
    if json_duplicate_ids:
        report["errors"].append("JSON index contains duplicate IDs.")
    if html_duplicate_ids:
        report["errors"].append("HTML atlas contains duplicate IDs.")
    if json_duplicate_sources:
        report["errors"].append("JSON index contains duplicate canonical source URLs.")
    if invalid_sources:
        report["errors"].append("One or more records have a missing or invalid source URL.")
    if not ids_match:
        report["errors"].append("JSON and HTML record IDs differ in count, content, or order.")
    if field_mismatches:
        report["errors"].append("JSON and HTML source, thumbnail, or red-warning fields differ.")
    if red_warning_gaps:
        report["errors"].append("Records describing extra elements lack red_warning_required=true.")

    if no_thumbnail:
        report["warnings"].append(
            f"{len(no_thumbnail)} records have no direct thumbnail; this is not counted as a broken image."
        )
    if unverified_thumbnails:
        report["warnings"].append(
            f"{len(unverified_thumbnails)} thumbnail URLs remain unverified or have only candidate metadata."
        )
    if unverified_license_status:
        report["warnings"].append(
            f"{len(unverified_license_status)} records have missing, pending, or unverified license-status metadata."
        )
    if duplicate_thumbnail_groups:
        report["warnings"].append(
            f"{len(duplicate_thumbnail_groups)} exact thumbnail URL group(s) are shared by multiple records; review before deduplication."
        )

    report["ok"] = not report["errors"]
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Check KIRA Atlas JSON/HTML census consistency without networking or downloading images."
    )
    parser.add_argument("--json", dest="json_path", type=Path, default=DEFAULT_JSON, help="Path to the visual census JSON.")
    parser.add_argument("--html", dest="html_path", type=Path, default=DEFAULT_HTML, help="Path to the interactive census HTML.")
    parser.add_argument("--json-output", type=Path, help="Optional path to save the audit report as JSON.")
    args = parser.parse_args(argv)

    report = audit_documents(args.json_path, args.html_path)
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(output + "\n", encoding="utf-8")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
