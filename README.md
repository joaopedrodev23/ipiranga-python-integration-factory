# ipiranga-python-integration-factory

> **Internal Developer Platform** — microservice generator for the Ipiranga Integration Factory.

---

## Project Purpose

This repository provides a **command-line code generator** that scaffolds
production-ready Python microservices from a concise YAML specification.
Engineers describe *what* a service should do; the generator produces *how*
it does it — FastAPI application, Pydantic models, HTTP/database/messaging
clients, Docker configuration, and more.

The goal is to eliminate boilerplate, enforce architectural standards, and
dramatically reduce the time from specification to a deployable service.

---

## Generator Concept

```
YAML Spec  ──►  Loader  ──►  Validator  ──►  Renderer  ──►  Generated Project
```

| Layer | Responsibility |
|-------|---------------|
| **Loader** (`spec_loader.py`) | Reads and parses the YAML file |
| **Validator** (`validators.py`) | Enforces required fields and allowed values |
| **Scaffold** (`scaffold.py`) | Creates the output directory tree |
| **Renderer** (`renderers/`) | Writes source files from templates + spec data |

---

## Planned Scenarios

### Phase 1 — REST Microservices *(in progress)*

Generates a FastAPI service that exposes an HTTP endpoint and proxies
requests to a downstream REST API.

Spec keys: `service`, `http.inbound`, `integration` (target_type: rest)

### Phase 2 — Database CRUD Microservices *(planned)*

Generates a FastAPI service with full Create / Read / Update / Delete
endpoints backed by a relational database (SQLAlchemy + Alembic migrations).

Spec keys: `service`, `http.inbound`, `database`

### Phase 3 — Kafka Listener Services *(planned)*

Generates a service that consumes messages from a Kafka topic and persists
them to a relational database.

Spec keys: `service`, `kafka.consumer`, `database`

---

## Repository Structure

```
ipiranga-python-integration-factory/
├── generator/
│   ├── __init__.py
│   ├── cli.py            # CLI entry point (--spec / --output)
│   ├── spec_loader.py    # YAML loader
│   ├── validators.py     # Spec validation rules
│   ├── scaffold.py       # Filesystem utilities
│   └── renderers/
│       ├── __init__.py
│       └── rest_renderer.py   # Phase 1 renderer (placeholder)
├── templates/
│   └── rest/             # Jinja2 templates for REST services (Phase 1)
├── examples/
│   └── rest_service.yml  # Reference spec for a REST microservice
├── tests/
│   ├── test_spec_loader.py
│   ├── test_validators.py
│   └── test_scaffold.py
├── README.md
└── pyproject.toml
```

---

## Requirements

- **Python 3.13+**
- **PyYAML 6.0+**

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

Or, after installing the package:

```bash
integration-factory \
  --spec examples/rest_service.yml \
  --output ./generated
```

### Expected output (Phase 0 — foundation only)

```
[1/4] Loading spec from: examples/rest_service.yml
[2/4] Validating spec …
      ✔ service.name = 'example-service'
      ✔ service.type = 'rest'
[3/4] Spec is valid — service 'example-service' (type: rest)
[4/4] Preparing output directory: ./generated
      ✔ Output directory ready: /path/to/generated

Foundation phase complete. Generation not yet implemented.
```

---

## Running Tests

```bash
pytest
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

## Contributing

1. Follow the existing module structure.
2. All new code must be fully typed (`from __future__ import annotations`).
3. Add tests for every new validator or scaffold utility.
4. Do **not** add database or Kafka support until Phase 2 / Phase 3 are
   formally scoped.

---

*Maintained by the Ipiranga Platform Engineering team.*
