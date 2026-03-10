"""
Tests for generator.renderers.rest_renderer.RestRenderer.
"""

from pathlib import Path

import pytest

from generator.renderers.rest_renderer import RestRenderer

VALID_SPEC: dict = {
    "service": {"name": "my-service", "type": "rest"},
    "http": {"inbound": {"path": "/hello", "method": "GET"}},
    "integration": {
        "target_type": "rest",
        "base_url": "https://backend.example.com",
        "endpoint_path": "/api/v1",
    },
}


def test_render_creates_service_directory(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    assert (tmp_path / "my-service").is_dir()


def test_render_creates_app_main_py(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    assert (tmp_path / "my-service" / "app" / "main.py").is_file()


def test_render_creates_requirements_txt(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    assert (tmp_path / "my-service" / "requirements.txt").is_file()


def test_render_creates_readme(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    assert (tmp_path / "my-service" / "README.md").is_file()


def test_placeholder_service_name_replaced(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    content = (tmp_path / "my-service" / "app" / "main.py").read_text()
    assert "my-service" in content
    assert "{{ service_name }}" not in content


def test_placeholder_http_method_lower_replaced(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    content = (tmp_path / "my-service" / "app" / "main.py").read_text()
    assert "@app.get(" in content
    assert "{{ http_method_lower }}" not in content


def test_placeholder_inbound_path_replaced(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    content = (tmp_path / "my-service" / "app" / "main.py").read_text()
    assert '"/hello"' in content
    assert "{{ inbound_path }}" not in content


def test_placeholder_backend_url_replaced(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    content = (tmp_path / "my-service" / "app" / "main.py").read_text()
    assert "https://backend.example.com/api/v1" in content
    assert "{{ backend_base_url }}" not in content
    assert "{{ backend_endpoint_path }}" not in content


def test_no_placeholders_remain_in_readme(tmp_path: Path) -> None:
    RestRenderer(VALID_SPEC).render(str(tmp_path))
    content = (tmp_path / "my-service" / "README.md").read_text()
    assert "{{" not in content


def test_render_fails_if_destination_exists(tmp_path: Path) -> None:
    (tmp_path / "my-service").mkdir()
    with pytest.raises(FileExistsError, match="already exists"):
        RestRenderer(VALID_SPEC).render(str(tmp_path))
