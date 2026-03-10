"""
Tests for generator.validators.
"""

import pytest

from generator.validators import SpecValidationError, validate_spec

VALID_SPEC: dict = {
    "service": {"name": "example-service", "type": "rest"},
    "http": {"inbound": {"path": "/example", "method": "POST"}},
    "integration": {
        "target_type": "rest",
        "base_url": "https://api.example.com",
        "endpoint_path": "/backend",
    },
}


def test_valid_spec_passes() -> None:
    validate_spec(VALID_SPEC)


def test_valid_spec_with_optional_fields_passes() -> None:
    spec = {
        **VALID_SPEC,
        "service": {**VALID_SPEC["service"], "description": "My service"},
        "integration": {**VALID_SPEC["integration"], "mock_enabled": False},
    }
    validate_spec(spec)


# ---------- service block ----------

def test_missing_service_block_raises() -> None:
    with pytest.raises(SpecValidationError, match="service"):
        validate_spec({})


def test_missing_service_name_raises() -> None:
    spec = {**VALID_SPEC, "service": {"type": "rest"}}
    with pytest.raises(SpecValidationError, match="name"):
        validate_spec(spec)


def test_missing_service_type_raises() -> None:
    spec = {**VALID_SPEC, "service": {"name": "svc"}}
    with pytest.raises(SpecValidationError, match="type"):
        validate_spec(spec)


def test_unsupported_service_type_raises() -> None:
    spec = {**VALID_SPEC, "service": {"name": "svc", "type": "graphql"}}
    with pytest.raises(SpecValidationError, match="not supported"):
        validate_spec(spec)


def test_empty_service_name_raises() -> None:
    spec = {**VALID_SPEC, "service": {"name": "", "type": "rest"}}
    with pytest.raises(SpecValidationError, match="empty"):
        validate_spec(spec)


# ---------- http.inbound block ----------

def test_missing_http_inbound_path_raises() -> None:
    spec = {**VALID_SPEC, "http": {"inbound": {"method": "POST"}}}
    with pytest.raises(SpecValidationError, match="path"):
        validate_spec(spec)


def test_invalid_http_method_raises() -> None:
    spec = {**VALID_SPEC, "http": {"inbound": {"path": "/example", "method": "BREW"}}}
    with pytest.raises(SpecValidationError, match="not valid"):
        validate_spec(spec)


def test_all_valid_http_methods_accepted() -> None:
    for method in ("GET", "POST", "PUT", "PATCH", "DELETE"):
        spec = {**VALID_SPEC, "http": {"inbound": {"path": "/x", "method": method}}}
        validate_spec(spec)


# ---------- integration block ----------

def test_invalid_integration_target_type_raises() -> None:
    spec = {
        **VALID_SPEC,
        "integration": {**VALID_SPEC["integration"], "target_type": "grpc"},
    }
    with pytest.raises(SpecValidationError, match="not valid"):
        validate_spec(spec)


def test_missing_integration_base_url_raises() -> None:
    spec = {
        **VALID_SPEC,
        "integration": {"target_type": "rest", "endpoint_path": "/backend"},
    }
    with pytest.raises(SpecValidationError, match="base_url"):
        validate_spec(spec)


def test_missing_integration_endpoint_path_raises() -> None:
    spec = {
        **VALID_SPEC,
        "integration": {"target_type": "rest", "base_url": "https://api.example.com"},
    }
    with pytest.raises(SpecValidationError, match="endpoint_path"):
        validate_spec(spec)


def test_mock_enabled_non_boolean_raises() -> None:
    spec = {
        **VALID_SPEC,
        "integration": {**VALID_SPEC["integration"], "mock_enabled": "yes"},
    }
    with pytest.raises(SpecValidationError, match="boolean"):
        validate_spec(spec)


def test_mock_enabled_true_passes() -> None:
    spec = {
        **VALID_SPEC,
        "integration": {**VALID_SPEC["integration"], "mock_enabled": True},
    }
    validate_spec(spec)


def test_mock_enabled_false_passes() -> None:
    spec = {
        **VALID_SPEC,
        "integration": {**VALID_SPEC["integration"], "mock_enabled": False},
    }
    validate_spec(spec)
