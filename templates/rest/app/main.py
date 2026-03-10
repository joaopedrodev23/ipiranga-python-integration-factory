from fastapi import FastAPI

app = FastAPI(title="{{ service_name }}")

@app.{{ http_method_lower }}("{{ inbound_path }}")
def inbound():
    return {
        "service": "{{ service_name }}",
        "backend_url": "{{ backend_base_url }}{{ backend_endpoint_path }}",
        "status": "ok"
    }
