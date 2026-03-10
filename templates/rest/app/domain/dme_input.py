from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class DmeInput(BaseModel):
    """Generic DME-style inbound request model for {{ service_name }}."""

    header: dict[str, Any] | None = None
    payload: dict[str, Any]
