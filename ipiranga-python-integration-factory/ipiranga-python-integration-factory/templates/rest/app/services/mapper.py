from __future__ import annotations

from app.domain.dme_input import DmeInput
from app.domain.backend_payload import BackendPayload


def map_to_backend_payload(request: DmeInput) -> BackendPayload:
    """
    Map an inbound DmeInput into a BackendPayload.

    This mapper is intentionally explicit so it is easy to extend
    as the {{ service_name }} contract evolves.
    """
    data: dict = {}

    if request.header:
        data["header"] = request.header

    data.update(request.payload)

    return BackendPayload(data=data)
