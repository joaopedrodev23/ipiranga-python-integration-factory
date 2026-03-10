from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class BackendPayload(BaseModel):
    """Outbound payload model for {{ service_name }}."""

    data: dict[str, Any]
