"""Web build and debug leave font manifests to Flutter and declare local Roboto."""

import contextlib
from pathlib import Path
from types import SimpleNamespace

import pytest

from flet_cli.commands.build import Command as BuildCommand
from flet_cli.commands.debug import Command as DebugCommand

TEMPLATE = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
)
ROBOTO = {"family": "Roboto", "fonts": [{"asset": "web/assets/fonts/roboto.woff2"}]}
LUCIDE = {
    "family": "packages/lucide_icons_flutter/Lucide",
    "fonts": [{"asset": "packages/lucide_icons_flutter/assets/lucide.ttf"}],
}


def test_template_leaves_the_manifest_to_flutter():
    """No manifest in the template's `web/`: it would replace Flutter's."""
    assert (TEMPLATE / "web" / "assets" / "fonts" / "roboto.woff2").exists()
    assert not (TEMPLATE / "web" / "assets" / "FontManifest.json").exists()


@pytest.fixture(params=[BuildCommand, DebugCommand], ids=["build", "debug-release"])
def command(request, tmp_path, monkeypatch):
    import cookiecutter.main

    cmd = request.param.__new__(request.param)
    cmd.build_dir = tmp_path / "build"
    cmd.flutter_dir = cmd.build_dir / "flutter"
    cmd.pubspec_path = str(cmd.flutter_dir / "pubspec.yaml")
    cmd.options = SimpleNamespace(
        template=str(tmp_path / "template"),
        template_ref=None,
        template_dir=None,
        no_cdn=False,
        release=True,
    )
    cmd.template_data = {"project_name": "test_app", "no_cdn": False}
    cmd.get_pyproject = lambda *_: None
    cmd.config_platform = "web"
    cmd.required_flutter_version = "3.47.9"
    cmd.emojis = {"checkmark": ""}
    cmd.verbose = 0
    cmd.step = lambda *_: contextlib.nullcontext()
    cmd.rendered = {}

    def render(**_):
        cmd.flutter_dir.mkdir(parents=True, exist_ok=True)
        Path(cmd.pubspec_path).write_text("name: test_app\ndependencies: {}\n")
        for rel, text in cmd.rendered.items():
            path = cmd.flutter_dir / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        font = cmd.flutter_dir / "web/assets/fonts/roboto.woff2"
        font.parent.mkdir(parents=True, exist_ok=True)
        font.write_bytes((TEMPLATE / "web/assets/fonts/roboto.woff2").read_bytes())

    monkeypatch.setattr(cookiecutter.main, "cookiecutter", render)
    return cmd


def _fonts(command):
    return command.load_yaml(command.pubspec_path).get("flutter", {}).get("fonts", [])


class TestBundledRoboto:
    """Roboto must be declared before Flutter runs, including in debug mode."""

    @pytest.mark.parametrize("setting", ["cli", "pyproject"])
    def test_no_cdn_declares_bundled_roboto(self, command, setting):
        command.options.no_cdn = setting == "cli"
        command.get_pyproject = lambda key: (
            False if setting == "pyproject" and key == "tool.flet.web.cdn" else None
        )
        command.template_data["no_cdn"] = command.resolve_no_cdn()

        assert command.create_flutter_project()
        assert command.create_flutter_project(second_pass=True)
        assert not command.create_flutter_project()

        assert _fonts(command) == [ROBOTO]
        assert (command.flutter_dir / ROBOTO["fonts"][0]["asset"]).is_file()
        assert command.load_yaml(f"{command.pubspec_path}.orig")["flutter"][
            "fonts"
        ] == [ROBOTO]

    def test_preserves_configured_fonts(self, command):
        command.template_data["no_cdn"] = True
        command.get_pyproject = lambda key: (
            {"flutter": {"fonts": [LUCIDE]}}
            if key == "tool.flet.flutter.pubspec"
            else None
        )

        assert command.create_flutter_project()

        assert _fonts(command) == [LUCIDE, ROBOTO]

    def test_keeps_custom_roboto(self, command):
        command.template_data["no_cdn"] = True
        custom = {"family": "Roboto", "fonts": [{"asset": "fonts/custom.ttf"}]}
        command.get_pyproject = lambda key: (
            {"flutter": {"fonts": [custom]}}
            if key == "tool.flet.flutter.pubspec"
            else None
        )

        assert command.create_flutter_project()

        assert _fonts(command) == [custom]

    def test_switching_back_to_cdn_removes_bundled_roboto(self, command):
        command.template_data["no_cdn"] = True
        assert command.create_flutter_project()

        command.template_data["no_cdn"] = False
        assert command.create_flutter_project()

        assert _fonts(command) == []

    def test_cdn_leaves_roboto_to_flutter(self, command):
        assert command.create_flutter_project()

        assert _fonts(command) == []

    def test_native_does_not_bundle_roboto(self, command):
        command.config_platform = "macos"
        command.template_data["no_cdn"] = True

        assert command.create_flutter_project()

        assert _fonts(command) == []


class TestStaleManifest:
    """A manifest an older template left in the reused Flutter project."""

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
