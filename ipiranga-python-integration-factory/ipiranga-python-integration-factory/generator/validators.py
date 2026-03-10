"""
Specification validators.

Each public function accepts the parsed spec dict and raises a descriptive
exception when a required field is absent or holds an invalid value.
Additional validators for future phases (database, Kafka) will be added here.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Supported values
# ---------------------------------------------------------------------------
SUPPORTED_SERVICE_TYPES: frozenset[str] = frozenset({"rest"})
SUPPORTED_HTTP_METHODS: frozenset[str] = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE"})
SUPPORTED_TARGET_TYPES: frozenset[str] = frozenset({"rest"})


class SpecValidationError(ValueError):
    """Raised when a loaded spec fails semantic validation."""


def _require_field(mapping: dict, *keys: str, context: str = "spec") -> None:
    """
    Assert that a chain of nested keys exists and is non-empty.

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

    Required: service.name, service.type
    Optional: service.description (any non-empty string)
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


def validate_rest_block(spec: dict) -> None:
    """
    Validate REST-specific blocks when service.type == "rest".

    Required:
        http.inbound.path, http.inbound.method,
        integration.target_type, integration.base_url, integration.endpoint_path

    Optional:
        integration.mock_enabled (must be boolean if present)
    """
    # http.inbound block
    _require_field(spec, "http", context="spec")
    _require_field(spec, "http", "inbound", context="spec")
    _require_field(spec, "http", "inbound", "path", context="spec")
    _require_field(spec, "http", "inbound", "method", context="spec")

    method: str = spec["http"]["inbound"]["method"]
    if method not in SUPPORTED_HTTP_METHODS:
        supported = ", ".join(sorted(SUPPORTED_HTTP_METHODS))
        raise SpecValidationError(
            f"[spec] http.inbound.method '{method}' is not valid. "
            f"Supported values: {supported}."
        )

    # integration block
    _require_field(spec, "integration", context="spec")
    _require_field(spec, "integration", "target_type", context="spec")
    _require_field(spec, "integration", "base_url", context="spec")
    _require_field(spec, "integration", "endpoint_path", context="spec")

    target_type: str = spec["integration"]["target_type"]
    if target_type not in SUPPORTED_TARGET_TYPES:
        supported = ", ".join(sorted(SUPPORTED_TARGET_TYPES))
        raise SpecValidationError(
            f"[spec] integration.target_type '{target_type}' is not valid. "
            f"Supported values: {supported}."
        )

    # Optional: mock_enabled must be boolean if provided
    mock_enabled = spec["integration"].get("mock_enabled")
    if mock_enabled is not None and not isinstance(mock_enabled, bool):
        raise SpecValidationError(
            f"[spec] integration.mock_enabled must be a boolean (true/false), "
            f"got {type(mock_enabled).__name__}: {mock_enabled!r}."
        )


def validate_spec(spec: dict) -> None:
    """
    Run all validators against *spec*.

    This is the single entry-point called by the CLI.
    """
    validate_service_block(spec)

    service_type: str = spec["service"]["type"]
    if service_type == "rest":
        validate_rest_block(spec)
