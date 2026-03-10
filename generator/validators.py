"""
Specification validators.

Each public function accepts the parsed spec dict and raises a descriptive
exception when a required field is absent or holds an invalid value.
Additional validators for future phases (database, Kafka) will be added here.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Supported service types — extend when new phases are implemented
# ---------------------------------------------------------------------------
SUPPORTED_SERVICE_TYPES: frozenset[str] = frozenset({"rest"})


class SpecValidationError(ValueError):
    """Raised when a loaded spec fails semantic validation."""


def _require_field(mapping: dict, *keys: str, context: str = "spec") -> None:
    """
    Assert that a chain of nested keys exists and is non-empty.

    Args:
        mapping: The (possibly nested) dict to inspect.
        *keys:   Ordered key path, e.g. ``"service", "name"``.
        context: Human-readable label used in error messages.

    Raises:
        SpecValidationError: If any key in the chain is missing or blank.
    """
    current: object = mapping
    path = ""

    for key in keys:
        path = f"{path}.{key}" if path else key

        if not isinstance(current, dict):
            raise SpecValidationError(
                f"[{context}] Expected a mapping at '{path}', "
                f"got {type(current).__name__}."
            )

        if key not in current:
            raise SpecValidationError(
                f"[{context}] Required field '{path}' is missing."
            )

        current = current[key]

    if current is None or (isinstance(current, str) and not current.strip()):
        raise SpecValidationError(
            f"[{context}] Required field '{path}' must not be empty."
        )


def validate_service_block(spec: dict) -> None:
    """
    Validate the top-level ``service`` block.

    Required fields
    ---------------
    - service.name   — non-empty string identifier
    - service.type   — must be one of :data:`SUPPORTED_SERVICE_TYPES`

    Args:
        spec: Full parsed spec dictionary.

    Raises:
        SpecValidationError: On any validation failure.
    """
    _require_field(spec, "service", context="spec")
    _require_field(spec, "service", "name", context="spec")
    _require_field(spec, "service", "type", context="spec")

    service_type: str = spec["service"]["type"]
    if service_type not in SUPPORTED_SERVICE_TYPES:
        supported = ", ".join(sorted(SUPPORTED_SERVICE_TYPES))
        raise SpecValidationError(
            f"[spec] service.type '{service_type}' is not supported. "
            f"Supported values: {supported}."
        )


def validate_spec(spec: dict) -> None:
    """
    Run all validators against *spec*.

    This is the single entry-point called by the CLI.  Additional phase
    validators should be invoked from here once implemented.

    Args:
        spec: Full parsed spec dictionary.

    Raises:
        SpecValidationError: If any validation rule is violated.
    """
    validate_service_block(spec)
