"""
REST microservice renderer — Phase 1 placeholder.

This module will contain the logic that translates a validated REST spec
into a fully functional FastAPI microservice project on disk.

Current state
-------------
The class is a typed placeholder only.  No generation logic is implemented.
The ``render`` method logs its intent and returns without writing any files.

Planned responsibilities (do NOT implement yet)
-----------------------------------------------
- Render ``main.py`` with a FastAPI application and the configured HTTP routes.
- Render ``models.py`` with Pydantic request/response models derived from the spec.
- Render ``client.py`` with an ``httpx``-based integration client for the
  downstream ``integration.target_type == "rest"`` target.
- Render ``pyproject.toml`` / ``Dockerfile`` for the generated service.
- Copy or render Jinja2 templates from ``templates/rest/``.
"""

from __future__ import annotations


class RestRenderer:
    """
    Renders a REST microservice from a validated spec dictionary.

    Args:
        spec: Fully validated specification dictionary produced by
              :func:`generator.validators.validate_spec`.
    """

    def __init__(self, spec: dict) -> None:
        self._spec = spec

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def render(self, output_dir: str) -> None:
        """
        Generate all source files for the REST microservice into *output_dir*.

        .. note::
            Generation logic is **not yet implemented**.
            This method is a placeholder for Phase 1 development.

        Args:
            output_dir: Absolute or relative path to the target directory.
                        The directory is expected to exist before this method
                        is called (see :func:`generator.scaffold.create_output_dir`).
        """
        service_name: str = self._spec.get("service", {}).get("name", "<unknown>")
        # TODO (Phase 1): implement FastAPI project generation
        print(
            f"[RestRenderer] render() called for service '{service_name}' "
            f"→ output_dir='{output_dir}' (not yet implemented)"
        )

    # ------------------------------------------------------------------
    # Private helpers (stubs for future implementation)
    # ------------------------------------------------------------------

    def _render_main(self, output_dir: str) -> None:
        """Render ``main.py`` with the FastAPI application. (TODO)"""
        raise NotImplementedError

    def _render_models(self, output_dir: str) -> None:
        """Render ``models.py`` with Pydantic schemas. (TODO)"""
        raise NotImplementedError

    def _render_client(self, output_dir: str) -> None:
        """Render ``client.py`` with the downstream HTTP integration client. (TODO)"""
        raise NotImplementedError
