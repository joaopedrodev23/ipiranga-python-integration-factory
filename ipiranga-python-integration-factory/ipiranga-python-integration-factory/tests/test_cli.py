"""
CLI smoke tests.
"""

import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEC_FILE = REPO_ROOT / "examples" / "rest_service.yml"


def test_cli_generates_service_directory(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable, "-m", "generator.cli",
            "--spec", str(SPEC_FILE),
            "--output", str(tmp_path),
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode == 0, f"CLI failed:\n{result.stderr}"
    assert (tmp_path / "example-service").is_dir()


def test_cli_generates_app_main_py(tmp_path: Path) -> None:
    subprocess.run(
        [
            sys.executable, "-m", "generator.cli",
            "--spec", str(SPEC_FILE),
            "--output", str(tmp_path),
        ],
        check=True,
        cwd=str(REPO_ROOT),
    )
    assert (tmp_path / "example-service" / "app" / "main.py").is_file()


def test_cli_missing_spec_exits_nonzero(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable, "-m", "generator.cli",
            "--spec", str(tmp_path / "nonexistent.yml"),
            "--output", str(tmp_path),
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode != 0
    assert "ERROR" in result.stderr


def test_cli_invalid_spec_exits_nonzero(tmp_path: Path) -> None:
    bad_spec = tmp_path / "bad.yml"
    bad_spec.write_text("service:\n  name: svc\n  type: rest\n", encoding="utf-8")
    result = subprocess.run(
        [
            sys.executable, "-m", "generator.cli",
            "--spec", str(bad_spec),
            "--output", str(tmp_path / "out"),
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    assert result.returncode != 0
    assert "ERROR" in result.stderr


def test_cli_output_contains_no_unicode_checkmarks(tmp_path: Path) -> None:
    result = subprocess.run(
        [
            sys.executable, "-m", "generator.cli",
            "--spec", str(SPEC_FILE),
            "--output", str(tmp_path),
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    combined = result.stdout + result.stderr
    assert "\u2714" not in combined, "Unicode checkmark found in CLI output"
    assert "\u2026" not in combined, "Unicode ellipsis found in CLI output"
