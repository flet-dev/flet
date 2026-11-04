import pytest
from fastapi.testclient import TestClient

from flet_web.fastapi import FastAPI


@pytest.mark.parametrize(
    ("kwargs", "expected_root_path"),
    [
        ({}, ""),
        ({"root_path": "/app"}, "/app"),
        ({"openapi_prefix": "/legacy"}, "/legacy"),
        ({"openapi_prefix": "/legacy", "root_path": "/app"}, "/app"),
    ],
)
def test_fastapi_root_path_and_lifecycle(kwargs, expected_root_path):
    """`root_path` falls back to `openapi_prefix`, and lifecycle hooks run once."""
    events = []
    app = FastAPI(
        **kwargs,
        on_startup=[lambda: events.append("startup")],
        on_shutdown=[lambda: events.append("shutdown")],
    )

    @app.get("/path")
    def get_root_path():
        return {"root_path": app.root_path}

    with TestClient(app) as client:
        assert events == ["startup"]
        response = client.get("/path")
        assert response.status_code == 200
        assert response.json() == {"root_path": expected_root_path}

    assert events == ["startup", "shutdown"]
