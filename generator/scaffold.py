"""
Scaffold utilities.

Low-level helpers for preparing the output filesystem before renderers
write generated files into it.  All functions are intentionally stateless
and side-effect free apart from filesystem operations.
"""

from __future__ import annotations

import os
from pathlib import Path


def create_output_dir(path: str) -> Path:
    """
    Ensure that *path* (and any intermediate directories) exists on disk.

    This function is idempotent: calling it on an already-existing directory
    is a no-op and does not raise an error.

    Args:
        path: Filesystem path of the directory to create.

    Returns:
        A :class:`pathlib.Path` object pointing to the resolved directory.

    Raises:
        OSError: If the directory cannot be created due to permissions or
                 other OS-level constraints.
    """
    target = Path(path).resolve()
    target.mkdir(parents=True, exist_ok=True)
    return target


def ensure_dir(path: str | Path) -> Path:
    """
    Convenience wrapper — identical to :func:`create_output_dir` but also
    accepts a :class:`pathlib.Path` argument.

    Args:
        path: Directory path (str or Path).

    Returns:
        Resolved :class:`pathlib.Path` of the created/existing directory.
    """
    return create_output_dir(str(path))


def write_file(output_dir: str | Path, filename: str, content: str) -> Path:
    """
    Write *content* to ``<output_dir>/<filename>``, creating the parent
    directory if necessary.

    Args:
        output_dir: Base directory for the output file.
        filename:   Relative file name (may include sub-directories).
        content:    Text content to write, encoded as UTF-8.

    Returns:
        Resolved :class:`pathlib.Path` of the written file.
    """
    target_dir = ensure_dir(output_dir)
    file_path = (target_dir / filename).resolve()

    # Ensure any sub-directories inside filename exist
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_text(content, encoding="utf-8")
    return file_path
