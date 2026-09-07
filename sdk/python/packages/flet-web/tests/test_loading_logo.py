import importlib
import shutil
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

static_files = importlib.import_module("flet_web.fastapi.flet_static_files")
CLIENT_WEB = Path(__file__).resolve().parents[5] / "client" / "web"


@pytest.mark.parametrize("custom_logo", [False, True])
def test_dynamic_loading_logo_respects_assets_override(
    tmp_path, monkeypatch, custom_logo
):
    web = tmp_path / "web"
    shutil.copytree(CLIENT_WEB, web)
    # Flutter substitutes this token before packaging the dynamic client.
    index = web / "index.html"
    index.write_text(index.read_text().replace("$FLUTTER_BASE_HREF", "/"))
    monkeypatch.setattr(static_files, "get_package_web_dir", lambda: str(web))
    assets = tmp_path / "assets"
    assets.mkdir()
    relative = Path("icons/loading-animation.png")
    expected = (CLIENT_WEB / relative).read_bytes()
    if custom_logo:
        # Serving must preserve the user's bytes instead of regenerating the logo.
        expected = b"custom loading logo"
        (assets / "icons").mkdir()
        (assets / relative).write_bytes(expected)

    app = FastAPI()
    app.mount("/demo", static_files.FletStaticFiles(assets_dir=str(assets)))
    with TestClient(app) as client:
        page = client.get("/demo/nested/route")
        assert page.status_code == 200
        assert '<base href="/demo/">' in page.text
        assert 'src="icons/loading-animation.png"' in page.text
        assert "@keyframes" not in page.text
        logo = client.get("/demo/icons/loading-animation.png")
        assert logo.status_code == 200
        assert logo.content == expected
