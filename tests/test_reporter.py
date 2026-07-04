"""
tests/test_reporter.py – Tests for scanner/reporter.py

Verifies export functions and the stable JSON contract.
"""

import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import pytest

from scanner.reporter import (
    export_json,
    export_csv,
    generate_json_report,
    generate_error_report,
    write_json_report,
    dumps_compact,
)


# ── Fixtures ───────────────────────────────────────────────────────────────
SAMPLE_FINDINGS = [
    {
        "type": "Hardcoded Password",
        "severity": "HIGH",
        "file": "app/settings.py",
        "line": 12,
        "content": 'pass***d = "hun***2"',
    },
    {
        "type": "AWS Access Key",
        "severity": "HIGH",
        "file": "config/aws.py",
        "line": 5,
        "content": "AKI***ODNN7EXAM***E",
    },
]


# ── generate_json_report ───────────────────────────────────────────────────
class TestGenerateJsonReport:
    def test_success_is_true(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10)
        assert report["success"] is True

    def test_scanner_metadata(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10)
        assert report["scanner"]["name"] == "secret-scanner"
        assert report["scanner"]["version"] == "1.0.0"

    def test_scan_target(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10)
        assert report["scan"]["target"] == "/tmp/project"

    def test_scan_duration(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 1234, 10)
        assert report["scan"]["duration_ms"] == 1234

    def test_scan_timestamp_format(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10)
        ts = report["scan"]["timestamp"]
        datetime.strptime(ts, "%Y-%m-%dT%H:%M:%SZ")

    def test_summary_counts(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 100, 5)
        assert report["summary"]["files_scanned"] == 100
        assert report["summary"]["files_ignored"] == 5
        assert report["summary"]["secrets_found"] == 2
        assert report["summary"]["errors"] == 0

    def test_findings_have_ids(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10)
        assert report["findings"][0]["id"] == "SEC-001"
        assert report["findings"][1]["id"] == "SEC-002"

    def test_findings_map_fields(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10)
        f = report["findings"][0]
        assert f["type"] == "Hardcoded Password"
        assert f["severity"] == "HIGH"
        assert f["file"] == "app/settings.py"
        assert f["line"] == 12
        assert f["match"] == 'pass***d = "hun***2"'

    def test_empty_findings(self):
        report = generate_json_report([], "/tmp/project", 100, 10)
        assert report["findings"] == []
        assert report["summary"]["secrets_found"] == 0

    def test_errors_list(self):
        errors = [{"file": "bad.py", "error": "permission denied"}]
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10, errors=errors)
        assert report["summary"]["errors"] == 1
        assert report["errors"] == errors

    def test_ignored_files_empty(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10)
        assert report["ignored_files"] == []

    def test_is_serializable(self):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp/project", 500, 10)
        raw = json.dumps(report, ensure_ascii=False)
        parsed = json.loads(raw)
        assert parsed["success"] is True


# ── generate_error_report ──────────────────────────────────────────────────
class TestGenerateErrorReport:
    def test_success_is_false(self):
        report = generate_error_report("SCAN_ERROR", "Ruta no encontrada")
        assert report["success"] is False

    def test_error_fields(self):
        report = generate_error_report("SCAN_ERROR", "Ruta no encontrada")
        assert report["error"]["code"] == "SCAN_ERROR"
        assert report["error"]["message"] == "Ruta no encontrada"

    def test_is_serializable(self):
        report = generate_error_report("SCAN_ERROR", "test")
        raw = json.dumps(report, ensure_ascii=False)
        parsed = json.loads(raw)
        assert parsed["success"] is False


# ── write_json_report ──────────────────────────────────────────────────────
class TestWriteJsonReport:
    def test_creates_file(self, tmp_path):
        report = generate_json_report([], "/tmp", 0, 0)
        out = str(tmp_path / "report.json")
        write_json_report(report, out)
        assert Path(out).exists()

    def test_content_is_valid_json(self, tmp_path):
        report = generate_json_report(SAMPLE_FINDINGS, "/tmp", 100, 10)
        out = str(tmp_path / "report.json")
        write_json_report(report, out)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        assert data["success"] is True

    def test_creates_parent_directory(self, tmp_path):
        report = generate_json_report([], "/tmp", 0, 0)
        out = str(tmp_path / "a" / "b" / "report.json")
        write_json_report(report, out)
        assert Path(out).exists()


# ── dumps_compact ──────────────────────────────────────────────────────────
class TestDumpsCompact:
    def test_returns_string(self):
        result = dumps_compact({"key": "value"})
        assert isinstance(result, str)

    def test_is_valid_json(self):
        result = dumps_compact({"key": "value"})
        parsed = json.loads(result)
        assert parsed["key"] == "value"

    def test_no_extra_whitespace(self):
        result = dumps_compact({"a": 1})
        assert "\n" not in result

    def test_ensure_ascii_false(self):
        result = dumps_compact({"msg": "nino"})
        assert "nino" in result


# ── export_json (legacy) ──────────────────────────────────────────────────
class TestExportJSON:
    def test_creates_file(self, tmp_path):
        out = str(tmp_path / "output" / "report.json")
        export_json(SAMPLE_FINDINGS, out)
        assert Path(out).exists()

    def test_creates_parent_directory(self, tmp_path):
        nested = str(tmp_path / "a" / "b" / "c" / "report.json")
        export_json(SAMPLE_FINDINGS, nested)
        assert Path(nested).exists()

    def test_content_is_valid_json(self, tmp_path):
        out = str(tmp_path / "report.json")
        export_json(SAMPLE_FINDINGS, out)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        assert isinstance(data, list)

    def test_content_matches_findings(self, tmp_path):
        out = str(tmp_path / "report.json")
        export_json(SAMPLE_FINDINGS, out)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        assert len(data) == len(SAMPLE_FINDINGS)
        assert data[0]["type"] == SAMPLE_FINDINGS[0]["type"]
        assert data[0]["line"] == SAMPLE_FINDINGS[0]["line"]

    def test_empty_findings_produces_empty_list(self, tmp_path):
        out = str(tmp_path / "empty.json")
        export_json([], out)
        with open(out, encoding="utf-8") as fh:
            data = json.load(fh)
        assert data == []

    def test_json_is_indented(self, tmp_path):
        out = str(tmp_path / "pretty.json")
        export_json(SAMPLE_FINDINGS, out)
        raw = Path(out).read_text(encoding="utf-8")
        assert "\n" in raw


# ── export_csv (legacy) ───────────────────────────────────────────────────
class TestExportCSV:
    def test_creates_file(self, tmp_path):
        out = str(tmp_path / "output" / "report.csv")
        export_csv(SAMPLE_FINDINGS, out)
        assert Path(out).exists()

    def test_creates_parent_directory(self, tmp_path):
        nested = str(tmp_path / "deep" / "dir" / "report.csv")
        export_csv(SAMPLE_FINDINGS, nested)
        assert Path(nested).exists()

    def test_has_header_row(self, tmp_path):
        out = str(tmp_path / "report.csv")
        export_csv(SAMPLE_FINDINGS, out)
        with open(out, newline="", encoding="utf-8") as fh:
            reader = csv.reader(fh)
            header = next(reader)
        assert "type" in header
        assert "severity" in header
        assert "file" in header
        assert "line" in header
        assert "content" in header

    def test_row_count_matches_findings(self, tmp_path):
        out = str(tmp_path / "report.csv")
        export_csv(SAMPLE_FINDINGS, out)
        with open(out, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == len(SAMPLE_FINDINGS)

    def test_content_matches_findings(self, tmp_path):
        out = str(tmp_path / "report.csv")
        export_csv(SAMPLE_FINDINGS, out)
        with open(out, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert rows[0]["type"] == SAMPLE_FINDINGS[0]["type"]
        assert int(rows[0]["line"]) == SAMPLE_FINDINGS[0]["line"]

    def test_empty_findings_produces_only_header(self, tmp_path):
        out = str(tmp_path / "empty.csv")
        export_csv([], out)
        with open(out, newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        assert rows == []
