"""The fonts a `flet build web` app loads: Flutter's generated `FontManifest.json`."""

import argparse
import contextlib
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from flet_cli.commands.build_base import BaseBuildCommand

TEMPLATE = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
)
ROBOTO = {"family": "Roboto", "fonts": [{"asset": "fonts/roboto.woff2"}]}
LUCIDE = {
    "family": "packages/lucide_icons_flutter/Lucide",
    "fonts": [{"asset": "packages/lucide_icons_flutter/assets/lucide.ttf"}],
}


def test_template_leaves_the_manifest_to_flutter():
    """No manifest in the template's `web/`: it would replace Flutter's."""
    assert (TEMPLATE / "web" / "assets" / "fonts" / "roboto.woff2").exists()
    assert not (TEMPLATE / "web" / "assets" / "FontManifest.json").exists()


@pytest.fixture
def web_command(tmp_path):
    cmd = BaseBuildCommand(argparse.ArgumentParser())
    cmd.options = argparse.Namespace(no_cdn=False)
    cmd.get_pyproject = lambda *_: None
    cmd.out_dir = tmp_path / "out"
    (cmd.out_dir / "assets").mkdir(parents=True)
    return cmd


def _write_manifest(cmd, fonts):
    (cmd.out_dir / "assets" / "FontManifest.json").write_text(json.dumps(fonts))


def _manifest(cmd):
    return json.loads((cmd.out_dir / "assets" / "FontManifest.json").read_text())


class TestBundledRoboto:
    """`add_bundled_roboto_font()` adding Roboto to Flutter's manifest."""

    def test_no_cdn_adds_roboto_after_the_package_fonts(self, web_command):
        web_command.options.no_cdn = True
        _write_manifest(web_command, [LUCIDE])

        web_command.add_bundled_roboto_font()
        web_command.add_bundled_roboto_font()

        assert _manifest(web_command) == [LUCIDE, ROBOTO]

    def test_pyproject_cdn_false_adds_roboto(self, web_command):
        web_command.get_pyproject = (
            lambda key: False if key == "tool.flet.web.cdn" else None
        )
        _write_manifest(web_command, [LUCIDE])

        web_command.add_bundled_roboto_font()

        assert _manifest(web_command) == [LUCIDE, ROBOTO]

    def test_cdn_build_keeps_flutters_manifest(self, web_command):
        _write_manifest(web_command, [LUCIDE])

        web_command.add_bundled_roboto_font()

        assert _manifest(web_command) == [LUCIDE]

    def test_no_manifest_is_left_alone(self, web_command):
        web_command.options.no_cdn = True

        web_command.add_bundled_roboto_font()

        assert not (web_command.out_dir / "assets" / "FontManifest.json").exists()


class TestStaleManifest:
    """A manifest an older template left in the reused Flutter project."""

    @pytest.fixture
    def command(self, tmp_path, monkeypatch):
        import cookiecutter.main

        cmd = BaseBuildCommand.__new__(BaseBuildCommand)
        cmd.build_dir = tmp_path / "build"
        cmd.flutter_dir = cmd.build_dir / "flutter"
        cmd.pubspec_path = str(cmd.flutter_dir / "pubspec.yaml")
        cmd.options = SimpleNamespace(
            template=str(tmp_path / "template"), template_ref=None, template_dir=None
        )
        cmd.template_data = {"project_name": "test_app"}
        cmd.get_pyproject = lambda *_: None
        cmd.config_platform = "web"
        cmd.required_flutter_version = "3.47.9"
        cmd.emojis = {"checkmark": ""}
        cmd.verbose = 0
        cmd.step = lambda *_: contextlib.nullcontext()
        cmd.rendered = {}

        def render(**_):
            # Writes the template's files, then a manifest if it has one.
            cmd.flutter_dir.mkdir(parents=True, exist_ok=True)
            Path(cmd.pubspec_path).write_text("name: test_app\ndependencies: {}\n")
            for rel, text in cmd.rendered.items():
                path = cmd.flutter_dir / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)

        monkeypatch.setattr(cookiecutter.main, "cookiecutter", render)
        return cmd

    def test_render_removes_a_manifest_the_template_no_longer_has(self, command):
        stale = command.flutter_dir / "web" / "assets" / "FontManifest.json"
        stale.parent.mkdir(parents=True)
        stale.write_text("[]")

        assert command.create_flutter_project()

        assert not stale.exists()

    def test_a_template_with_a_manifest_keeps_it(self, command):
        manifest = command.flutter_dir / "web" / "assets" / "FontManifest.json"
        command.rendered = {"web/assets/FontManifest.json": "[1]"}

        assert command.create_flutter_project()

        assert manifest.read_text() == "[1]"
