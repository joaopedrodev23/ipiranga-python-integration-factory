# ipiranga-python-integration-factory

> **Internal Developer Platform** - microservice generator for the Ipiranga Integration Factory.

---

## Project Purpose

This repository provides a **command-line code generator** that scaffolds
production-ready Python microservices from a concise YAML specification.
Engineers describe *what* a service should do; the generator produces *how*
it does it - FastAPI application, integration client, dependency files, and more.

The goal is to eliminate boilerplate, enforce architectural standards, and
dramatically reduce the time from specification to a deployable service.

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
| Renderer | `renderers/` | Writes source files from templates + spec data |

---

## Supported Scenarios

### Phase 1 - REST Microservices (IMPLEMENTED)

Generates a FastAPI service that exposes an HTTP endpoint and proxies
requests to a downstream REST API.

Required spec keys: `service`, `http.inbound`, `integration` (target_type: rest)

Supported HTTP methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`

### Phase 2 - Database CRUD Microservices (planned)

Generates a FastAPI service with full CRUD endpoints backed by a relational
database (SQLAlchemy + Alembic migrations).

### Phase 3 - Kafka Listener Services (planned)

Generates a service that consumes messages from a Kafka topic and persists
them to a relational database.

---

## Repository Structure

```
ipiranga-python-integration-factory/
├── generator/
│   ├── __init__.py
│   ├── cli.py              # CLI entry point (--spec / --output)
│   ├── spec_loader.py      # YAML loader
│   ├── validators.py       # Spec validation rules
│   ├── scaffold.py         # Filesystem utilities
│   └── renderers/
│       ├── __init__.py
│       └── rest_renderer.py    # Phase 1 REST renderer
├── templates/
│   └── rest/               # Templates for REST services
│       ├── app/
│       │   └── main.py
│       ├── requirements.txt
│       └── README.md
├── examples/
│   └── rest_service.yml    # Reference spec for a REST microservice
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

Install all dependencies (including dev tools):

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

Or after installing the package:

```bash
integration-factory \
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
│   └── main.py         # FastAPI application with configured route
├── requirements.txt    # Runtime dependencies (fastapi, uvicorn)
└── README.md           # Service-specific readme
```

### Example `app/main.py` (generated from `rest_service.yml`)

```python
from fastapi import FastAPI

app = FastAPI(title="example-service")

@app.post("/example")
def inbound():
    return {
        "service": "example-service",
        "backend_url": "https://api.example.com/backend",
        "status": "ok"
    }
```

---

## Example Spec (`examples/rest_service.yml`)

```yaml
service:
  name: example-service
  type: rest

http:
  inbound:
    path: /example
    method: POST

integration:
  target_type: rest
  base_url: https://api.example.com
  endpoint_path: /backend
```

---

## Running Tests

```bash
pytest
```

All 34 tests should pass.

---

## Supported Spec Placeholders

| Placeholder | Source field |
|-------------|-------------|
| `{{ service_name }}` | `service.name` |
| `{{ inbound_path }}` | `http.inbound.path` |
| `{{ http_method }}` | `http.inbound.method` |
| `{{ http_method_lower }}` | `http.inbound.method.lower()` |
| `{{ backend_base_url }}` | `integration.base_url` |
| `{{ backend_endpoint_path }}` | `integration.endpoint_path` |

Placeholder replacement is applied to files with extensions: `.py`, `.txt`, `.md`, `.yml`, `.yaml`

---

*Maintained by the Ipiranga Platform Engineering team.*
