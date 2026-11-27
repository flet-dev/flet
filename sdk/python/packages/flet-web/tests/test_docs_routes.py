"""Flet web apps don't serve FastAPI's interactive docs (/docs, /redoc, /openapi.json).

Those routes are registered before the static files mounted at "/", so they would
take a page route like "/docs" away from the app and load Swagger UI/ReDoc from a CDN.
"""

import importlib

import pytest
from fastapi.testclient import TestClient

import flet_web.fastapi as flet_fastapi
from flet_web.fastapi.serve_fastapi_web_app import get_fastapi_web_app

static_files = importlib.import_module("flet_web.fastapi.flet_static_files")

INDEX = "<html><head></head><body>flet app</body></html>"
DOCS_ROUTES = ["/docs", "/redoc", "/openapi.json"]
PAGE_ROUTES = ["/docs", "/redoc"]


def main(page):
    pass


@pytest.fixture(autouse=True)
def web(tmp_path, monkeypatch):
    """A packaged web client directory with just an index page."""
    web = tmp_path / "web"
    web.mkdir()
    (web / "index.html").write_text(INDEX)
    (web / "manifest.json").write_text("{}")
    monkeypatch.setattr(static_files, "get_package_web_dir", lambda: str(web))
    return web


def flet_run_web_app(tmp_path):
    return get_fastapi_web_app(
        main,
        before_main=None,
        page_name="",
        assets_dir=str(tmp_path),
        upload_dir=None,
    )


@pytest.fixture(params=["app", "flet_run_web"])
def client(request, tmp_path):
    """The app from `flet_web.fastapi.app()` and the one `flet run --web` serves."""
    if request.param == "app":
        app = flet_fastapi.app(main)
    else:
        app = flet_run_web_app(tmp_path)
    with TestClient(app) as client:
        yield client


@pytest.mark.parametrize("path", DOCS_ROUTES)
def test_docs_are_not_served(client, path):
    text = client.get(path).text.lower()
    assert "swagger" not in text
    assert "redoc" not in text
    assert '"openapi"' not in text


@pytest.mark.parametrize("path", PAGE_ROUTES)
def test_app_route_named_like_docs_serves_the_app(client, path):
    response = client.get(path)
    assert response.status_code == 200
    assert "flet app" in response.text


def test_own_fastapi_app_keeps_its_docs():
    """Only the apps Flet creates drop the docs; a user's own FastAPI() keeps them."""
    app = flet_fastapi.FastAPI()
    with TestClient(app) as client:
        assert client.get("/docs").status_code == 200
        assert client.get("/openapi.json").status_code == 200
