"""
Tests for generator.spec_loader.
"""

import textwrap
from pathlib import Path

import pytest

from generator.spec_loader import load_spec


def test_load_valid_spec(tmp_path: Path) -> None:
    yaml_file = tmp_path / "spec.yml"
    yaml_file.write_text(
        textwrap.dedent("""\
            service:
              name: my-service
              type: rest
        """),
        encoding="utf-8",
    )
    spec = load_spec(str(yaml_file))
    assert spec["service"]["name"] == "my-service"
    assert spec["service"]["type"] == "rest"


def test_load_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        load_spec("/nonexistent/path/spec.yml")


def test_load_empty_file(tmp_path: Path) -> None:
    empty = tmp_path / "empty.yml"
    empty.write_text("", encoding="utf-8")
    with pytest.raises(ValueError, match="empty"):
        load_spec(str(empty))


def test_load_non_mapping_file(tmp_path: Path) -> None:
    bad = tmp_path / "bad.yml"
    bad.write_text("- item1\n- item2\n", encoding="utf-8")
    with pytest.raises(ValueError, match="mapping"):
        load_spec(str(bad))
