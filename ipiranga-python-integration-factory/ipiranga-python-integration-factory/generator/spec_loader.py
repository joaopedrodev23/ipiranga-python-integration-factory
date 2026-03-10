"""
YAML specification loader.

Responsible for reading a YAML file from disk and returning its contents
as a plain Python dictionary. All I/O and parsing errors are surfaced here
so the rest of the pipeline can work with clean data.
"""

from pathlib import Path

import yaml


def load_spec(path: str) -> dict:
    """
    Load a YAML specification file and return its contents as a dictionary.

    Args:
        path: Filesystem path to the YAML file.

    Returns:
        Parsed YAML contents as a dict.

    Raises:
        FileNotFoundError: If the file does not exist at *path*.
        ValueError: If the file is empty or does not parse to a mapping.
        yaml.YAMLError: If the file contains invalid YAML syntax.
    """
    spec_path = Path(path)

    if not spec_path.exists():
        raise FileNotFoundError(f"Spec file not found: {spec_path.resolve()}")

    if not spec_path.is_file():
        raise ValueError(f"Path is not a regular file: {spec_path.resolve()}")

    raw = spec_path.read_text(encoding="utf-8")

    parsed = yaml.safe_load(raw)

    if parsed is None:
        raise ValueError(f"Spec file is empty: {spec_path.resolve()}")

    if not isinstance(parsed, dict):
        raise ValueError(
            f"Spec file must be a YAML mapping at the top level, "
            f"got {type(parsed).__name__}: {spec_path.resolve()}"
        )

    return parsed
