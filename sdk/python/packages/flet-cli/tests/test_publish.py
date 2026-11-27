"""`flet publish`."""

import argparse
import json
import shutil
from pathlib import Path

import pytest

import flet.utils.pip
import flet_web
from flet_cli.commands.publish import Command

PACKAGE_WEB_DIR = Path(flet_web.get_package_web_dir())


@pytest.fixture
def publish(tmp_path, monkeypatch):
    """Run `flet publish` on an app with the given `pyproject.toml`.

    Returns the published `manifest.json`.
    """
    web_dir = tmp_path / "web"
    web_dir.mkdir()
    for name in ("index.html", "manifest.json"):
        shutil.copy(PACKAGE_WEB_DIR / name, web_dir / name)
    monkeypatch.setattr(flet_web, "get_package_web_dir", lambda: str(web_dir))
    monkeypatch.setattr(
        flet.utils.pip, "ensure_flet_web_package_installed", lambda: None
    )

    def run(pyproject: str, *args: str) -> dict:
        app_dir = tmp_path / "app"
        app_dir.mkdir()
        (app_dir / "main.py").write_text("import flet as ft\n", encoding="utf-8")
        (app_dir / "pyproject.toml").write_text(pyproject, encoding="utf-8")
        parser = argparse.ArgumentParser()
        command = Command(parser)
        command.handle(parser.parse_args([str(app_dir / "main.py"), *args]))
        manifest = app_dir / "dist" / "manifest.json"
        return json.loads(manifest.read_text(encoding="utf-8"))

    return run


class TestPublishManifestNames:
    def test_pwa_short_name_from_pyproject(self, publish):
        """`[tool.flet.web].pwa_short_name` sets `short_name`, not `name`."""
        manifest = publish(
            '[project]\nname = "cool_counter"\n\n'
            '[tool.flet.web]\npwa_short_name = "Short"\n'
        )
        assert manifest["short_name"] == "Short"
        assert manifest["name"] == "cool_counter"

    def test_app_short_name_flag_wins(self, publish):
        """`--app-short-name` takes precedence over `pwa_short_name`."""
        manifest = publish(
            '[project]\nname = "cool_counter"\n\n'
            '[tool.flet.web]\npwa_short_name = "Short"\n',
            "--app-short-name",
            "FromCli",
        )
        assert manifest["short_name"] == "FromCli"

    def test_short_name_defaults_to_product(self, publish):
        """Without a short name, `short_name` is the product name."""
        manifest = publish(
            '[project]\nname = "cool_counter"\n\n'
            '[tool.flet]\nproduct = "Cool Counter"\n'
        )
        assert manifest["short_name"] == "Cool Counter"
        assert manifest["name"] == "Cool Counter"

    def test_short_name_defaults_to_project_name(self, publish):
        """Without a short name or product, `short_name` is the project name."""
        manifest = publish('[project]\nname = "cool_counter"\n')
        assert manifest["short_name"] == "cool_counter"
