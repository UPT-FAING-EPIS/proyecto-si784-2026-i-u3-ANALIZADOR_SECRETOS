"""
reporter.py – Export scan findings to JSON or CSV files.

Provides the stable JSON contract consumed by Electron / CDS Antivirus.
"""

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

OUTPUT_DIR = "output"
SCANNER_VERSION = "1.0.0"


def _ensure_output_dir(output_path: str) -> None:
    """Create the parent directory for *output_path* if it does not exist."""
    parent = Path(output_path).parent
    parent.mkdir(parents=True, exist_ok=True)


def generate_json_report(
    findings: List[Dict[str, Any]],
    target: str,
    duration_ms: int,
    files_scanned: int,
    files_ignored: int = 0,
    errors: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Any]:
    """Build the stable JSON report contract.

    Parameters
    ----------
    findings : list[dict]
        List of finding dicts as returned by ``scan_path``.
    target : str
        Scanned path (absolute or relative).
    duration_ms : int
        Scan duration in milliseconds.
    files_scanned : int
        Number of files actually scanned.
    files_ignored : int
        Number of files skipped (binary, permission, etc.).
    errors : list[dict] | None
        Non-fatal errors encountered during the scan.

    Returns
    -------
    dict
        Serializable dictionary matching the CDS Antivirus contract.
    """
    report_findings: List[Dict[str, Any]] = []
    for idx, f in enumerate(findings, start=1):
        report_findings.append(
            {
                "id": f"SEC-{idx:03d}",
                "type": f.get("type", "UNKNOWN"),
                "severity": f.get("severity", "MEDIUM"),
                "file": f.get("file", ""),
                "line": f.get("line", 0),
                "match": f.get("content", ""),
            }
        )

    return {
        "success": True,
        "scanner": {
            "name": "secret-scanner",
            "version": SCANNER_VERSION,
        },
        "scan": {
            "target": target,
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "duration_ms": duration_ms,
        },
        "summary": {
            "files_scanned": files_scanned,
            "files_ignored": files_ignored,
            "secrets_found": len(findings),
            "errors": len(errors) if errors else 0,
        },
        "findings": report_findings,
        "ignored_files": [],
        "errors": errors or [],
    }


def generate_error_report(code: str, message: str) -> Dict[str, Any]:
    """Build an error report following the JSON contract.

    Parameters
    ----------
    code : str
        Machine-readable error code (e.g. ``"SCAN_ERROR"``).
    message : str
        Human-readable description.

    Returns
    -------
    dict
        Error contract dictionary.
    """
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
        },
    }


def export_json(findings: List[Dict[str, Any]], output_path: str) -> None:
    """Serialize *findings* to a JSON file at *output_path*.

    The output directory is created automatically when it does not exist.

    Parameters
    ----------
    findings : list[dict]
        List of finding dicts as returned by ``scan_path``.
    output_path : str
        Destination file path (e.g. ``"output/report.json"``).
    """
    _ensure_output_dir(output_path)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(findings, fh, indent=2, ensure_ascii=False)


def export_csv(findings: List[Dict[str, Any]], output_path: str) -> None:
    """Write *findings* to a CSV file at *output_path*.

    The output directory is created automatically when it does not exist.

    Parameters
    ----------
    findings : list[dict]
        List of finding dicts as returned by ``scan_path``.
    output_path : str
        Destination file path (e.g. ``"output/report.csv"``).
    """
    _ensure_output_dir(output_path)

    fieldnames = ["type", "severity", "file", "line", "content"]

    with open(output_path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(findings)


def print_json_report(findings: List[Dict[str, Any]]) -> None:
    """Print *findings* as a formatted JSON string to stdout.

    Parameters
    ----------
    findings : list[dict]
        List of finding dicts as returned by ``scan_path``.
    """
    print(json.dumps(findings, indent=2, ensure_ascii=False))


def write_json_report(report: Dict[str, Any], output_path: str) -> None:
    """Write a full report dict to *output_path* as compact JSON.

    Parameters
    ----------
    report : dict
        Report dictionary (from ``generate_json_report``).
    output_path : str
        Destination file path.
    """
    _ensure_output_dir(output_path)
    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False)


def dumps_compact(obj: Any) -> str:
    """Serialize *obj* to a compact JSON string (no extra whitespace).

    Parameters
    ----------
    obj : any
        JSON-serializable object.

    Returns
    -------
    str
        Compact JSON string.
    """
    return json.dumps(obj, ensure_ascii=False)
