from __future__ import annotations

from app.domain.backend_payload import BackendPayload

MOCK_ENABLED: bool = {{ integration_mock_enabled }}
BACKEND_URL: str = "{{ backend_base_url }}{{ backend_endpoint_path }}"


def call_backend(payload: BackendPayload) -> dict:
    """
    Forward the mapped payload to the backend REST service.

    When MOCK_ENABLED is True, returns a local mock response without
    making a real HTTP call.  This is the expected behaviour in dev/hml.
    """
    if MOCK_ENABLED:
        return {
            "mock": True,
            "payload_received": payload.data,
        }

    # TODO: implement real HTTP call when mock_enabled is false.
    # Example:
    #   import httpx
    #   response = httpx.post(BACKEND_URL, json=payload.data)
    #   response.raise_for_status()
    #   return response.json()
    return {
        "mock": False,
        "backend_url": BACKEND_URL,
        "payload": payload.data,
        "note": "Real HTTP call not yet implemented.",
    }
