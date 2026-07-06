"""
test_web_api.py - Unit tests for the Web API handlers and calculations.
"""

import pytest
from fastapi import UploadFile, HTTPException
import io

from secret_scanner.web.app import (
    calculate_entropy_metrics,
    scan_raw_text,
    check_entropy,
    generate_secret,
    scan_code,
    get_patterns,
    check_custom_pattern,
    EntropyRequest,
    GenerateSecretRequest,
    ScanCodeRequest,
    CustomPatternRequest,
    scan_github_repository,
    ScanGitRequest,
    scan_zip_upload,
)

def test_calculate_entropy_metrics_empty():
    res = calculate_entropy_metrics("")
    assert res["shannon_entropy"] == 0.0
    assert res["pool_entropy_bits"] == 0.0
    assert res["strength"] == "Vacio"
    assert "vacío" in res["recommendations"][0]

def test_calculate_entropy_metrics_weak():
    res = calculate_entropy_metrics("12345")
    assert res["strength"] == "Muy Débil"
    assert len(res["recommendations"]) > 0

def test_calculate_entropy_metrics_strong():
    res = calculate_entropy_metrics("aB3$eF8*1qW5!xP9")
    # Should be relatively strong
    assert res["pool_entropy_bits"] > 60
    assert "Fuerte" in res["strength"]

def test_scan_raw_text_clean():
    findings = scan_raw_text("def my_func():\n    return True")
    assert len(findings) == 0

def test_scan_raw_text_with_secrets():
    code = (
        "# Config file\n"
        "github_token = 'ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'\n"
        "aws_key = 'AKIA1234567890123456'\n"
    )
    findings = scan_raw_text(code)
    assert len(findings) == 2
    assert findings[0]["type"] == "GitHub Token"
    assert findings[1]["type"] == "AWS Access Key"
    assert findings[0]["line"] == 2
    assert findings[1]["line"] == 3
    # Verify masking
    assert "***" in findings[0]["content"]

def test_get_patterns():
    patterns = get_patterns()
    assert len(patterns) >= 8
    assert any(p["name"] == "GitHub Token" for p in patterns)

def test_generate_secret():
    req = GenerateSecretRequest(length=24, use_symbols=False)
    res = generate_secret(req)
    secret = res["secret"]
    assert len(secret) == 24
    # No symbols should be present
    assert not any(c in "!@#$%^&*()_+=-[]{}|;:',.<>?/" for c in secret)
    assert res["metrics"]["pool_entropy_bits"] > 0

def test_scan_code_endpoint():
    req = ScanCodeRequest(code="password = 'my_super_secret_password'")
    res = scan_code(req)
    assert res["total_lines"] == 1
    assert len(res["findings"]) == 1
    assert res["findings"][0]["type"] == "Hardcoded Password"

def test_check_custom_pattern():
    req = CustomPatternRequest(pattern=r"token_[0-9]{3}", text="my token_123 here\nand token_abc there")
    res = check_custom_pattern(req)
    assert len(res["matches"]) == 1
    assert res["matches"][0]["match"] == "token_123"
    assert res["matches"][0]["line"] == 1

def test_scan_github_invalid_url():
    req = ScanGitRequest(clone_url="https://not-github.com/some/repo")
    with pytest.raises(HTTPException) as exc_info:
        scan_github_repository(req)
    assert exc_info.value.status_code == 400
    assert "URL de GitHub no válida" in exc_info.value.detail

def test_scan_zip_upload_invalid_extension():
    mock_file = UploadFile(filename="invalid.txt", file=io.BytesIO(b""))
    with pytest.raises(HTTPException) as exc_info:
        scan_zip_upload(mock_file)
    assert exc_info.value.status_code == 400
    assert "Tipo de archivo no permitido" in exc_info.value.detail
