"""
Tests for generator.scaffold.
"""

from pathlib import Path

from generator.scaffold import create_output_dir, write_file


def test_create_output_dir_creates_directory(tmp_path: Path) -> None:
    target = tmp_path / "a" / "b" / "c"
    result = create_output_dir(str(target))
    assert result.is_dir()


def test_create_output_dir_is_idempotent(tmp_path: Path) -> None:
    target = tmp_path / "output"
    create_output_dir(str(target))
    create_output_dir(str(target))  # second call must not raise
    assert target.is_dir()


def test_write_file_creates_file_with_content(tmp_path: Path) -> None:
    content = "hello, world\n"
    written = write_file(str(tmp_path), "sub/dir/hello.txt", content)
    assert written.is_file()
    assert written.read_text(encoding="utf-8") == content
