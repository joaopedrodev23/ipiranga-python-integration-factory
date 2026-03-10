"""
REST microservice renderer - Phase 1.

Translates a validated REST spec into a FastAPI microservice project on disk
by copying the templates/rest/ tree and replacing placeholders in text files.
"""

from __future__ import annotations

import shutil
from pathlib import Path

# File extensions that support placeholder replacement.
_TEXT_EXTENSIONS: frozenset[str] = frozenset({".py", ".txt", ".md", ".yml", ".yaml"})

# Absolute path to the templates/rest directory, resolved relative to this file.
_TEMPLATES_REST: Path = (
    Path(__file__).resolve().parent.parent.parent / "templates" / "rest"
)


class RestRenderer:
    """
    Renders a REST microservice from a validated spec dictionary.

    Args:
        spec: Fully validated specification dictionary produced by
              generator.validators.validate_spec.
    """

    def __init__(self, spec: dict) -> None:
        self._spec = spec

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, output_dir: str) -> None:
        """
        Generate all source files for the REST microservice into
        <output_dir>/<service_name>/.

        Args:
            output_dir: Base output directory (must already exist).

        Raises:
            FileExistsError: If the target service directory already exists.
            FileNotFoundError: If the REST template directory is missing.
        """
        placeholders = self._build_placeholders()
        service_name: str = placeholders["{{ service_name }}"]

        dest = Path(output_dir).resolve() / service_name

        if dest.exists():
            raise FileExistsError(
                f"[RestRenderer] Destination already exists: {dest}. "
                "Remove it or choose a different output directory."
            )

        template_dir = _TEMPLATES_REST
        if not template_dir.is_dir():
            raise FileNotFoundError(
                f"[RestRenderer] REST template directory not found: {template_dir}"
            )

        # Copy the entire template tree verbatim first.
        shutil.copytree(str(template_dir), str(dest))

        # Replace placeholders in all supported text files.
        for file_path in dest.rglob("*"):
            if file_path.is_file() and file_path.suffix in _TEXT_EXTENSIONS:
                self._replace_placeholders(file_path, placeholders)

        print(f"      [OK] Generated service directory: {dest}")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _build_placeholders(self) -> dict[str, str]:
        """Build the placeholder -> replacement mapping from the spec."""
        http_method: str = self._spec["http"]["inbound"]["method"]
        return {
            "{{ service_name }}": self._spec["service"]["name"],
            "{{ inbound_path }}": self._spec["http"]["inbound"]["path"],
            "{{ http_method }}": http_method,
            "{{ http_method_lower }}": http_method.lower(),
            "{{ backend_base_url }}": self._spec["integration"]["base_url"],
            "{{ backend_endpoint_path }}": self._spec["integration"]["endpoint_path"],
        }

    @staticmethod
    def _replace_placeholders(file_path: Path, placeholders: dict[str, str]) -> None:
        """Read *file_path*, replace all placeholders, and write back."""
        content = file_path.read_text(encoding="utf-8")
        for token, value in placeholders.items():
            content = content.replace(token, value)
        file_path.write_text(content, encoding="utf-8")
