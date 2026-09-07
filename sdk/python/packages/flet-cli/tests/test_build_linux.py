"""Tests concerning Linux `flet build` packaging."""

import argparse
import io
import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional
from unittest import mock

import pytest
import yaml
from flet_platform_assets import LINUX_HICOLOR_SIZES
from jinja2 import Environment, StrictUndefined
from PIL import Image

from flet_cli.commands import build_base
from flet_cli.commands.build_base import BaseBuildCommand

BUILD_TEMPLATE_DIR = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
)
TEMPLATE_PUBSPEC = BUILD_TEMPLATE_DIR / "pubspec.yaml"
TEMPLATE_DESKTOP_ENTRY = (
    BUILD_TEMPLATE_DIR / "linux" / "{{cookiecutter.bundle_id}}.desktop"
)


def _render_template(path: Path, **context: Any) -> str:
    """
    Render a build-template file the way cookiecutter would.

    Args:
        path: Template file to render.
        context: Values exposed to the template as `cookiecutter.*`.

    Returns:
        The rendered file content.
    """

    env = Environment(keep_trailing_newline=True, undefined=StrictUndefined)
    return env.from_string(path.read_text()).render(cookiecutter=context)


def _png_bytes(width: int = 256, height: int = 256) -> bytes:
    """
    Build a real, decodable PNG.

    A signature-plus-IHDR stub was enough while Linux only copied its icon,
    but generation now decodes every source, including for Linux.

    Args:
        width: Pixel width.
        height: Pixel height.

    Returns:
        The bytes of an encoded PNG.
    """

    buffer = io.BytesIO()
    Image.new("RGBA", (width, height), (255, 0, 85, 255)).save(buffer, format="PNG")
    return buffer.getvalue()


def _run_customize_icons(
    tmp_path: Path,
    *,
    assets: Optional[dict[str, bytes]] = None,
    target_platform: str = "linux",
    template_default_icon: bool = True,
) -> BaseBuildCommand:
    """
    Drive `BaseBuildCommand.customize_icons` against a faked project layout.

    Args:
        tmp_path: pytest tmp dir.
        assets: mapping of file name to content for the user's `assets` dir,
            or `None` for an app without an assets dir.
        target_platform: `flet build` target platform.
        template_default_icon: whether the rendered Flutter project ships
            the template's default `images/icon.png`.

    Returns:
        The faked command object, with `flutter_dir` and friends set.
    """

    app_path = tmp_path / "app"
    app_path.mkdir(parents=True, exist_ok=True)
    if assets is not None:
        assets_dir = app_path / "assets"
        assets_dir.mkdir(exist_ok=True)
        for name, content in assets.items():
            (assets_dir / name).write_bytes(content)

    flutter_dir = tmp_path / "flutter"
    (flutter_dir / "images").mkdir(parents=True, exist_ok=True)
    if template_default_icon:
        (flutter_dir / "images" / "icon.png").write_bytes(_png_bytes())
    (flutter_dir / "linux").mkdir(exist_ok=True)

    build_dir = tmp_path / "build"
    build_dir.mkdir(exist_ok=True)

    pubspec_path = flutter_dir / "pubspec.yaml"
    pubspec = yaml.safe_load(
        _render_template(
            TEMPLATE_PUBSPEC, project_name="test_app", pubspec_description=""
        )
    )
    pubspec_path.write_text(yaml.safe_dump(pubspec))
    (flutter_dir / "pubspec.yaml.orig").write_text(yaml.safe_dump(pubspec))

    cmd = BaseBuildCommand.__new__(BaseBuildCommand)
    cmd.package_app_path = app_path
    cmd.flutter_dir = flutter_dir
    cmd.build_dir = build_dir
    cmd.pubspec_path = str(pubspec_path)
    cmd.target_platform = target_platform
    cmd.config_platform = {"apk": "android", "aab": "android", "ipa": "ios"}.get(
        target_platform, target_platform
    )
    cmd.verbose = 0
    cmd.dart_exe = "dart"
    cmd.emojis = {"checkmark": "", "loading": ""}
    cmd.options = SimpleNamespace(android_adaptive_icon_background=None)
    cmd.template_data = {"bundle_id": "com.example.test_app"}
    cmd.template_digest = "test-template-digest"
    cmd.get_pyproject = lambda *_: None
    cmd.update_status = lambda *_: None
    cmd.run = lambda *a, **k: SimpleNamespace(returncode=0, stdout="", stderr="")
    cmd.customize_icons()
    return cmd


def _hicolor(cmd: BaseBuildCommand, size: int) -> Path:
    """One entry of the hicolor tree `customize_icons` renders."""

    return (
        cmd.flutter_dir
        / "linux"
        / "icons"
        / "hicolor"
        / f"{size}x{size}"
        / "apps"
        / "com.example.test_app.png"
    )


def _png_size(path: Path) -> tuple[int, int]:
    with Image.open(path) as img:
        return img.size


class TestLinuxIconGeneration:
    """
    The hicolor icon tree `customize_icons` renders for a Linux build.

    flutter_launcher_icons never had a Linux generator, so `flet build` used
    to install one file - often a 1024px image - into `hicolor/256x256/`. A
    directory that claims one size while holding another is rescaled wrongly
    by the icon cache, and every small panel size was downscaled from it on
    the fly.
    """

    def test_every_hicolor_size_matches_its_directory(self, tmp_path):
        cmd = _run_customize_icons(
            tmp_path, assets={"icon.png": _png_bytes(1024, 1024)}
        )
        for size in LINUX_HICOLOR_SIZES:
            assert _png_size(_hicolor(cmd, size)) == (size, size)

    def test_runner_window_icon_is_rendered(self, tmp_path):
        """my_application.cc loads this one directly at startup."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": _png_bytes()})
        assert _png_size(cmd.flutter_dir / "linux" / "app_icon.png") == (256, 256)

    def test_icon_linux_beats_the_generic_icon(self, tmp_path):
        """The platform-specific name wins, and only its chain is resolved."""
        cmd = _run_customize_icons(
            tmp_path,
            assets={
                "icon.png": _png_bytes(64, 64),
                "icon_linux.png": _png_bytes(512, 512),
            },
        )
        # Rendered from the 512 source, so the 512 entry is not an upscale of
        # the 64px generic one.
        assert _png_size(_hicolor(cmd, 512)) == (512, 512)

    def test_no_user_icon_generates_nothing(self, tmp_path):
        """Rule 2: the template's committed icons are better than anything
        derivable from a finished images/icon.png, and are left alone."""
        cmd = _run_customize_icons(tmp_path, assets=None)
        assert not (cmd.flutter_dir / "linux" / "icons").exists()

    def test_vector_only_assets_generate_nothing(self, tmp_path):
        """An SVG cannot be decoded, so there is no usable user icon."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.svg": b"<svg/>"})
        assert not (cmd.flutter_dir / "linux" / "icons").exists()

    def test_other_targets_do_not_render_linux_icons(self, tmp_path):
        cmd = _run_customize_icons(
            tmp_path, assets={"icon.png": _png_bytes()}, target_platform="windows"
        )
        assert not (cmd.flutter_dir / "linux" / "icons").exists()

    def test_regenerated_when_the_source_changes(self, tmp_path):
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": _png_bytes(256, 256)})
        assert _png_size(_hicolor(cmd, 512)) == (512, 512)

        icon = cmd.package_app_path / "assets" / "icon.png"
        icon.write_bytes(_png_bytes(64, 64))
        # Change detection keys on mtime; bump it explicitly so the test does
        # not depend on filesystem timestamp granularity.
        stat = icon.stat()
        os.utime(icon, (stat.st_atime, stat.st_mtime + 10))
        cmd.customize_icons()

        # Still the declared size, now upscaled from the smaller source.
        assert _png_size(_hicolor(cmd, 512)) == (512, 512)

    def test_unreadable_source_warns_without_failing(self, tmp_path, capsys):
        """A Pillow-vs-Dart decode divergence must never fail a build."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": b"not-actually-a-png"})
        assert not (cmd.flutter_dir / "linux" / "icons").exists()
        combined = capsys.readouterr()
        assert "could not read" in (combined.out + combined.err)


SENTINEL = b"stale-output-marker"


class TestGeneratorStamps:
    """
    What forces regeneration.

    Both are silent when wrong: the user keeps stale output and nothing
    reports it.
    """

    def test_template_rerender_forces_regeneration(self, tmp_path):
        """`create_flutter_project` re-renders with overwrite_if_exists=True,
        restoring the template's placeholder over generated output. Without
        the template digest in this stamp, generation is skipped and the
        artifacts silently stay reverted."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": _png_bytes()})
        generated = _hicolor(cmd, 256)
        generated.write_bytes(SENTINEL)  # stands in for the reverted file

        cmd.customize_icons()
        assert generated.read_bytes() == SENTINEL, "unchanged inputs should skip"

        cmd.template_digest = "a-different-template-digest"
        cmd.customize_icons()

        assert generated.read_bytes() != SENTINEL

    def test_generator_version_bump_forces_regeneration(self, tmp_path):
        """Nothing else encodes the generator's identity now that the pubspec
        does not, so upgrading flet-cli would otherwise keep stale pixels."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": _png_bytes()})
        generated = _hicolor(cmd, 256)
        generated.write_bytes(SENTINEL)

        cmd.customize_icons()
        assert generated.read_bytes() == SENTINEL, "unchanged inputs should skip"

        with mock.patch.object(build_base, "ICONS_GENERATOR_VERSION", 99):
            cmd.customize_icons()
        assert generated.read_bytes() != SENTINEL

    def test_missing_output_forces_regeneration(self, tmp_path):
        """An existence check catches output removed behind the stamp's back."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": _png_bytes()})
        for size in LINUX_HICOLOR_SIZES:
            _hicolor(cmd, size).unlink()

        cmd.customize_icons()

        assert _hicolor(cmd, 256).is_file()


class TestDesktopEntryEscaping:
    """
    `Exec` and `Categories`, which `flet build` escapes before rendering.

    Both pass through two layers — the entry file, where backslash is the
    escape character, and `Exec`'s shell-like parsing — and getting either
    wrong yields an entry the desktop environment silently discards.
    """

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("my_app", "my_app"),
            ("my app", "my app"),
            ('mid"dle', 'mid\\\\"dle'),
            ("my$app", "my\\\\$app"),
            ("a\\b", "a\\\\\\\\b"),
            ("tick`s", "tick\\\\`s"),
            # `%` starts a field code, so a literal one must be doubled or
            # the desktop drops it and the character after it.
            ("save 50% now", "save 50%% now"),
            ("100%", "100%%"),
        ],
    )
    def test_escape_linux_desktop_exec(self, raw, expected):
        """Reserved characters get a backslash, then every one is doubled."""
        assert BaseBuildCommand.escape_linux_desktop_exec(raw) == expected

    def test_escape_linux_desktop_categories(self):
        """Categories are semicolon-terminated, with separators escaped."""
        escape = BaseBuildCommand.escape_linux_desktop_categories
        assert escape(["Game", "Education"]) == "Game;Education;"
        assert escape("Development") == "Development;"
        # A literal ";" would otherwise split one category into two.
        assert escape(["Ut;ility"]) == "Ut\\;ility;"
        assert escape(["back\\slash"]) == "back\\\\slash;"
        assert escape(["Game", "  ", ""]) == "Game;"
        assert escape([]) == "Utility;"

    @pytest.mark.parametrize("bad", [5, None, ["ok", 7], {"a": 1}])
    def test_escape_linux_desktop_categories_rejects_non_strings(self, bad):
        """A malformed `pyproject.toml` value fails with a clear error instead of
        a jinja `TypeError`, which the build turns into a wiped build dir and
        a message that never mentions `pyproject.toml`."""
        with pytest.raises(ValueError):
            BaseBuildCommand.escape_linux_desktop_categories(bad)


class TestCategoriesResolution:
    """
    How `--linux-categories` and `[tool.flet.linux].categories` combine.

    The CLI option and the escaping are wired together in `setup_template_data`,
    so a test that only calls `escape_linux_desktop_categories` would pass even if the
    option were never added to the parser or never consulted.
    """

    @staticmethod
    def _parse(argv: list[str]) -> argparse.Namespace:
        """Build the real `flet build` parser and parse `argv` with it."""
        parser = argparse.ArgumentParser(add_help=False)
        BaseBuildCommand(parser)
        return parser.parse_args(argv)

    def test_fallback_matches_the_declared_default(self):
        """A non-Linux target still renders the desktop entry, so the fallback
        must equal `cookiecutter.json`'s default rather than override it with
        `None` — which rendered as the literal `Categories=None`."""
        declared = json.loads(
            (
                Path(__file__).resolve().parents[3]
                / "templates"
                / "build"
                / "cookiecutter.json"
            ).read_text()
        )["linux_categories"]
        assert BaseBuildCommand.escape_linux_desktop_categories(["Utility"]) == declared

    def test_option_is_registered(self):
        """The parser accepts the option and collects several values."""
        options = self._parse(["--linux-categories", "Game", "Education"])
        assert options.linux_categories == ["Game", "Education"]

    def test_option_repeats(self):
        """Repeating the flag extends rather than replaces, as its siblings do."""
        options = self._parse(
            ["--linux-categories", "Game", "--linux-categories", "Education"]
        )
        assert options.linux_categories == ["Game", "Education"]

    def test_option_defaults_to_empty(self):
        """Omitting it leaves an empty list, so pyproject is consulted next."""
        assert self._parse([]).linux_categories == []


class TestDesktopEntryTemplate:
    """
    Rendering of `linux/{{cookiecutter.bundle_id}}.desktop`, which is
    installed into `share/applications/` so desktop environments resolve the
    launcher name and icon from it.

    The template escapes every value it interpolates except `Exec` and
    `Categories`, which arrive pre-escaped from `flet build` — see
    `TestDesktopEntryEscaping`.
    """

    @staticmethod
    def _render(**overrides: str) -> str:
        """Render the entry with a cookiecutter-like context."""
        context = {
            "product_name": "My App",
            "project_description": "",
            "linux_desktop_exec": "my_app",
            "linux_categories": "Utility;",
            "bundle_id": "com.example.my_app",
            **overrides,
        }
        return _render_template(TEMPLATE_DESKTOP_ENTRY, **context)

    @staticmethod
    def _parse(content: str) -> dict:
        """
        Parse the entry the way a desktop environment does.

        Substring assertions cannot see whitespace-control mistakes: a group
        header glued onto the end of the preceding comment line still contains
        "[Desktop Entry]", but leaves every key outside any group and the whole
        file is ignored.
        """
        entry = {}
        in_section = False
        for line in content.splitlines():
            if line.startswith("[") and line.endswith("]"):
                in_section = line == "[Desktop Entry]"
                continue
            if in_section and "=" in line and not line.startswith("#"):
                key, _, value = line.partition("=")
                entry[key] = value
        return entry

    def test_group_header_starts_its_own_line(self):
        """The group header is not glued to the preceding comment block."""
        content = self._render()
        assert "\n[Desktop Entry]\n" in content, content[:400]

    def test_desktop_entry_fields(self):
        """Every key carries the value the build resolved for it."""
        entry = self._parse(self._render(project_description="Does great things."))
        assert entry["Type"] == "Application"
        assert entry["Name"] == "My App"
        assert entry["Comment"] == "Does great things."
        # Quoted, so an artifact name containing spaces stays one argument.
        assert entry["Exec"] == '"my_app" %U'
        # Icon and StartupWMClass are the bundle id: the runner sets its
        # program name to it, and that is how X11 and Wayland match a window
        # to this entry and its themed icon.
        assert entry["Icon"] == "com.example.my_app"
        assert entry["StartupWMClass"] == "com.example.my_app"
        assert entry["Categories"] == "Utility;"

    def test_comment_omitted_without_description(self):
        """An app with no description gets no empty `Comment` key."""
        content = self._render(project_description="")
        assert "Comment=" not in content
        # The conditional must not leave a blank line behind either.
        assert 'Name=My App\nExec="my_app" %U' in content

    def test_multiline_description_flattened(self):
        """
        Newlines are flattened: one inside `Comment` fails
        `desktop-file-validate` and the entry is ignored.
        """
        content = self._render(project_description="Line one.\nLine two.")
        assert "Comment=Line one. Line two." in content

    def test_control_characters_flattened_in_name_and_comment(self):
        """Tabs and newlines are flattened in both localestring keys."""
        content = self._render(
            product_name="My\tApp\nName", project_description="Tabbed\tdescription"
        )
        assert "Name=My App Name" in content
        assert "Comment=Tabbed description" in content

    def test_backslashes_escaped(self):
        """A literal backslash is doubled, as entry values use escapes."""
        content = self._render(project_description=r"Uses C:\path\now")
        assert r"Comment=Uses C:\\path\\now" in content

    def test_prepared_values_are_interpolated_verbatim(self):
        """`Exec` and `Categories` arrive escaped and are not escaped twice."""
        content = self._render(
            linux_desktop_exec=r"weird\\\"name", linux_categories="Game;Fun;"
        )
        assert 'Exec="weird\\\\\\"name" %U' in content
        assert "Categories=Game;Fun;" in content
