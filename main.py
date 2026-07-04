"""
main.py – SecretScanner CLI entry-point.

Usage
-----
    secret-scanner --target ./project
    secret-scanner --target ./project --format json
    secret-scanner --target ./project --format json --silent
    secret-scanner --target ./project --format json --output resultado.json
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

# Force UTF-8 output on Windows to avoid cp1252 UnicodeEncodeError
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
    except AttributeError:
        pass

from scanner.file_scanner import scan_path
from scanner.reporter import (
    generate_error_report,
    generate_json_report,
    write_json_report,
    dumps_compact,
)

# ── Lazy colorama import (only needed for text mode) ────────────────────────
_colorama = None


def _ensure_colorama() -> None:
    global _colorama
    if _colorama is None:
        try:
            import colorama
            colorama.init(autoreset=True)
            _colorama = colorama
        except ImportError:
            # Fallback: no colors available
            class _NoColor:
                class Fore:
                    RED = GREEN = YELLOW = CYAN = WHITE = BLUE = ""
                    class BRIGHT:
                        pass
                class Style:
                    BRIGHT = RESET_ALL = ""
            _colorama = _NoColor()


def _colored(text: str, color: str) -> str:
    return f"{color}{text}{_colorama.Style.RESET_ALL}"


def _banner() -> None:
    Fore = _colorama.Fore
    Style = _colorama.Style
    print(
        _colored(
            r"""
  ____  ___   ____ ____  _____ _____ ____   ____    _    _   _ _   _ _____ ____
 / ___||__ \ / ___| __ )| ____|_   _/ ___| / ___|  / \  | \ | | \ | | ____|  _ \
 \___ \  / // |   |  _ \|  _|   | | \___ \| |     / _ \ |  \| |  \| |  _| | |_) |
  ___) |/ /_| |___| |_) | |___  | |  ___) | |___ / ___ \| |\  | |\  | |___|  _ <
 |____//_____\____|____/|_____| |_| |____/ \____/_/   \_\_| \_|_| \_|_____|_| \_\
""",
            Fore.CYAN + Style.BRIGHT,
        )
    )
    print(_colored("  SecretScanner v1.0.0 - Hardcoded Secret Detector\n", Fore.WHITE))


# ── CLI argument parsing ─────────────────────────────────────────────────────


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="secret-scanner",
        description="Detect hardcoded secrets and credentials in source code.",
    )
    parser.add_argument(
        "--target",
        required=True,
        metavar="PATH",
        help="Directory or file to scan.",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format: 'text' (default) or 'json'.",
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Suppress all non-JSON output (for integration with Electron / CDS).",
    )
    parser.add_argument(
        "--output",
        default=None,
        metavar="FILE",
        help="Save JSON report to this file path.",
    )
    return parser


# ── Text-mode display helpers ────────────────────────────────────────────────

SEVERITY_COLOR = {}


def _init_severity_colors() -> None:
    Fore = _colorama.Fore
    Style = _colorama.Style
    SEVERITY_COLOR.update(
        {
            "HIGH": Fore.RED + Style.BRIGHT,
            "MEDIUM": Fore.YELLOW + Style.BRIGHT,
            "LOW": Fore.CYAN,
        }
    )


def _print_findings(findings: list) -> None:
    if not findings:
        return
    Fore = _colorama.Fore
    Style = _colorama.Style

    print(_colored("\n" + "-" * 70, Fore.WHITE))
    print(_colored("  FINDINGS", Fore.RED + Style.BRIGHT))
    print(_colored("-" * 70 + "\n", Fore.WHITE))

    for f in findings:
        severity = f.get("severity", "MEDIUM")
        color = SEVERITY_COLOR.get(severity, Fore.WHITE)
        badge = _colored(f"[{severity}]", color)
        type_label = _colored(f.get("type", "Unknown"), Fore.WHITE + Style.BRIGHT)
        file_info = _colored(f"{f['file']}:{f['line']}", Fore.BLUE)
        content = f.get("content", "")

        print(f"  {badge} {type_label}")
        print(f"    {_colored('File:', Fore.WHITE)} {file_info}")
        print(f"    {_colored('Content:', Fore.WHITE)} {content}")
        print()


def _print_summary(
    total_files: int,
    findings: list,
    output_path: str | None,
) -> None:
    Fore = _colorama.Fore
    Style = _colorama.Style
    count = len(findings)
    separator = "-" * 70

    print(_colored(separator, Fore.GREEN))

    if count == 0:
        print(
            _colored(
                "  [OK] No secrets found. Your project looks clean!",
                Fore.GREEN + Style.BRIGHT,
            )
        )
    else:
        print(
            _colored(
                f"  [!] {count} secret(s) found - review them before committing!",
                Fore.RED + Style.BRIGHT,
            )
        )

    print(_colored(f"  Files analysed : {total_files}", Fore.GREEN))
    print(_colored(f"  Secrets found  : {count}", Fore.GREEN))

    if output_path:
        print(_colored(f"  Report saved   : {output_path}", Fore.GREEN))

    print(_colored(separator, Fore.GREEN))


# ── Helpers ──────────────────────────────────────────────────────────────────


def _count_files(path: str) -> int:
    """Count scannable files under *path* (mirrors the scanner logic)."""
    root = Path(path).resolve()
    if root.is_file():
        return 1
    total = 0
    ignored_dirs = {
        ".git",
        "__pycache__",
        "node_modules",
        "output",
        ".venv",
        "venv",
        ".tox",
        "dist",
        "build",
        ".mypy_cache",
    }
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignored_dirs]
        total += len(filenames)
    return total


def _output_json(report: dict, output_path: str | None) -> None:
    """Write the JSON report to stdout and optionally to a file."""
    json_str = dumps_compact(report)
    print(json_str)
    if output_path:
        write_json_report(report, output_path)


def _emit_json_error(code: str, message: str, output_path: str | None = None) -> int:
    """Print a JSON error to stdout and return exit code 1."""
    report = generate_error_report(code, message)
    json_str = dumps_compact(report)
    print(json_str)
    if output_path:
        write_json_report(report, output_path)
    return 1


# ── Entry point ──────────────────────────────────────────────────────────────


def main() -> int:
    """CLI entry point. Returns an exit code (0 = clean, 1 = secrets or error)."""
    parser = _build_parser()
    args = parser.parse_args()

    is_json = args.format == "json"
    is_silent = args.silent
    output_path: str | None = args.output

    # ── Text mode setup ──
    if not is_json:
        _ensure_colorama()
        _init_severity_colors()
        _banner()

    # ── Validate target ──
    target = Path(args.target)
    if not target.exists():
        if is_json:
            return _emit_json_error("SCAN_ERROR", "Ruta no encontrada", output_path)
        else:
            _ensure_colorama()
            print(
                _colored(
                    f"  ERROR: Path not found: {args.target}",
                    _colorama.Fore.RED + _colorama.Style.BRIGHT,
                )
            )
            return 1

    # ── Scan ──
    if not is_json:
        print(_colored(f"  Scanning: {target.resolve()}", _colorama.Fore.CYAN))

    start_time = time.monotonic()

    try:
        findings = scan_path(
            str(target),
            verbose=not is_json and not is_silent,
        )
    except Exception as exc:
        if is_json:
            return _emit_json_error("SCAN_ERROR", str(exc), output_path)
        else:
            print(f"  ERROR: {exc}", file=sys.stderr)
            return 1

    duration_ms = int((time.monotonic() - start_time) * 1000)
    total_files = _count_files(str(target))

    # ── Build report ──
    report = generate_json_report(
        findings=findings,
        target=str(target.resolve()),
        duration_ms=duration_ms,
        files_scanned=total_files,
    )

    # ── Output ──
    if is_json:
        _output_json(report, output_path)
    else:
        _print_findings(findings)
        _print_summary(total_files, findings, output_path)

    return 1 if findings else 0


if __name__ == "__main__":
    main()
