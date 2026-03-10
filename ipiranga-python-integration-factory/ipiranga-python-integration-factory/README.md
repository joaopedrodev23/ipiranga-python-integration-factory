# ipiranga-python-integration-factory

> **Internal Developer Platform** - microservice generator for the Ipiranga Integration Factory.

---

## Project Purpose

This repository provides a **command-line code generator** that scaffolds
production-ready Python microservices from a concise YAML specification.
Engineers describe *what* a service should do; the generator produces *how*
it does it — a complete, layered FastAPI project ready to run.

---

## Generator Concept

```
YAML Spec  -->  Loader  -->  Validator  -->  Renderer  -->  Generated Project
```

| Layer | File | Responsibility |
|-------|------|----------------|
| Loader | `spec_loader.py` | Reads and parses the YAML file |
| Validator | `validators.py` | Enforces required fields and allowed values |
| Scaffold | `scaffold.py` | Creates the output directory tree |
| Renderer | `renderers/rest_renderer.py` | Copies templates and replaces placeholders |

---

## Supported Scenarios

### Phase 1.1 — REST Microservices (IMPLEMENTED)

Generates an enterprise-style FastAPI service that exposes a typed HTTP
endpoint and integrates with a downstream REST backend.

The generated project follows a layered architecture:

| Layer | Directory | Purpose |
|-------|-----------|---------|
| API | `app/api/` | FastAPI router and inbound endpoint |
| Domain | `app/domain/` | Pydantic request/response models |
| Services | `app/services/` | Request mapping logic |
| Integrations | `app/integrations/` | Outbound backend stub |
| Settings | `settings.*.yml` | Per-environment configuration |

### Phase 2 — Database CRUD Microservices (planned)

Generates a FastAPI service with full CRUD endpoints backed by a relational
database (SQLAlchemy + Alembic migrations).

### Phase 3 — Kafka Listener Services (planned)

Generates a service that consumes messages from a Kafka topic and persists
them to a relational database.

---

## Repository Structure

```
ipiranga-python-integration-factory/
├── generator/
│   ├── cli.py                  # CLI entry point (--spec / --output)
│   ├── spec_loader.py          # YAML loader
│   ├── validators.py           # Spec validation rules
│   ├── scaffold.py             # Filesystem utilities
│   └── renderers/
│       └── rest_renderer.py    # Phase 1.1 REST renderer
├── templates/
│   └── rest/                   # Template tree for REST services
│       ├── app/
│       │   ├── main.py
│       │   ├── api/inbound.py
│       │   ├── domain/
│       │   ├── services/mapper.py
│       │   └── integrations/outbound_rest.py
│       ├── settings.dev.yml
│       ├── settings.hml.yml
│       ├── settings.prod.yml
│       ├── requirements.txt
│       └── README.md
├── examples/
│   └── rest_service.yml        # Reference spec for a REST microservice
├── tests/
│   ├── test_cli.py
│   ├── test_rest_renderer.py
│   ├── test_scaffold.py
│   ├── test_spec_loader.py
│   └── test_validators.py
├── README.md
└── pyproject.toml
```

---

## Requirements

- Python 3.12+
- PyYAML 6.0+

```bash
pip install -e ".[dev]"
```

---

## CLI Usage

```bash
python -m generator.cli \
  --spec examples/rest_service.yml \
  --output ./generated
```

### CLI output

```
[1/4] Loading spec from: examples/rest_service.yml
[2/4] Validating spec ...
      [OK] service.name = 'example-service'
      [OK] service.type = 'rest'
[3/4] Preparing output directory: ./generated
      [OK] Output directory ready: /path/to/generated
[4/4] Generating rest service ...
      [OK] Generated service directory: /path/to/generated/example-service

Generated REST service: example-service
Output: /path/to/generated/example-service
```

---

## Generated Output Structure

```
generated/example-service/
├── app/
│   ├── __init__.py
│   ├── main.py                          # FastAPI app with router
│   ├── api/
│   │   ├── __init__.py
│   │   └── inbound.py                   # Inbound endpoint
│   ├── domain/
│   │   ├── __init__.py
│   │   ├── dme_input.py                 # Inbound Pydantic model
│   │   └── backend_payload.py           # Outbound Pydantic model
│   ├── services/
│   │   ├── __init__.py
│   │   └── mapper.py                    # Request mapping logic
│   └── integrations/
│       ├── __init__.py
│       └── outbound_rest.py             # Backend integration stub
├── settings.dev.yml
├── settings.hml.yml
├── settings.prod.yml
├── requirements.txt
└── README.md
```

### Running the generated service

```bash
cd generated/example-service
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Example Spec (`examples/rest_service.yml`)

```yaml
service:
  name: example-service
  type: rest
  description: "My integration service"   # optional

http:
  inbound:
    path: /example
    method: POST

integration:
  target_type: rest
  base_url: https://api.example.com
  endpoint_path: /backend
  mock_enabled: true                       # optional, default: true
```

### Optional spec fields

| Field | Default |
|-------|---------|
| `service.description` | `"Generated by ipiranga-python-integration-factory"` |
| `integration.mock_enabled` | `true` |

---

## Supported Placeholders

| Placeholder | Source |
|-------------|--------|
| `{{ service_name }}` | `service.name` |
| `{{ service_description }}` | `service.description` or default |
| `{{ inbound_path }}` | `http.inbound.path` |
| `{{ http_method }}` | `http.inbound.method` |
| `{{ http_method_lower }}` | `http.inbound.method.lower()` |
| `{{ backend_base_url }}` | `integration.base_url` |
| `{{ backend_endpoint_path }}` | `integration.endpoint_path` |
| `{{ integration_mock_enabled }}` | `integration.mock_enabled` or default |

Applied to files with extensions: `.py`, `.txt`, `.md`, `.yml`, `.yaml`

---

## Running Tests

```bash
pytest
```

49 tests, all passing.

---

*Maintained by the Ipiranga Platform Engineering team.*
