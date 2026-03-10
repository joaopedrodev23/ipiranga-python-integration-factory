"""
Renderers sub-package.

Each renderer is responsible for translating a validated spec dictionary
into concrete source files for a specific service archetype.

Planned renderers
-----------------
- :class:`~generator.renderers.rest_renderer.RestRenderer`   — Phase 1 (REST microservices)
- ``DatabaseRenderer``                                        — Phase 2 (DB CRUD microservices)
- ``KafkaRenderer``                                           — Phase 3 (Kafka → DB listener services)
"""

from generator.renderers.rest_renderer import RestRenderer

__all__: list[str] = ["RestRenderer"]
