"""
Tests for generator.validators.
"""

import pytest

from generator.validators import SpecValidationError, validate_spec


VALID_SPEC: dict = {
    "service": {
        "name": "example-service",
        "type": "rest",
    }
}


def test_valid_spec_passes() -> None:
    validate_spec(VALID_SPEC)  # should not raise


def test_missing_service_block_raises() -> None:
    with pytest.raises(SpecValidationError, match="service"):
        validate_spec({})


def test_missing_service_name_raises() -> None:
    with pytest.raises(SpecValidationError, match="name"):
        validate_spec({"service": {"type": "rest"}})


def test_missing_service_type_raises() -> None:
    with pytest.raises(SpecValidationError, match="type"):
        validate_spec({"service": {"name": "svc"}})


def test_unsupported_service_type_raises() -> None:
    with pytest.raises(SpecValidationError, match="not supported"):
        validate_spec({"service": {"name": "svc", "type": "graphql"}})


def test_empty_service_name_raises() -> None:
    with pytest.raises(SpecValidationError, match="empty"):
        validate_spec({"service": {"name": "", "type": "rest"}})
