from fastapi import APIRouter

from app.domain.dme_input import DmeInput
from app.services.mapper import map_to_backend_payload
from app.integrations.outbound_rest import call_backend

router = APIRouter()


@router.{{ http_method_lower }}("{{ inbound_path }}")
def inbound(request: DmeInput) -> dict:
    """
    Inbound endpoint for {{ service_name }}.
    Receives a DME-style request, maps it, and forwards to the backend.
    """
    payload = map_to_backend_payload(request)
    result = call_backend(payload)
    return {
        "service": "{{ service_name }}",
        "status": "ok",
        "result": result,
    }
