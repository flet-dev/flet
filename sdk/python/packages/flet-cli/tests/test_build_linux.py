"""Linux packaging in `flet build` (issue #2269).

Two halves, both driven against the real in-repo build template:

* **Icon staging** — `flutter_launcher_icons` has no Linux generator, so
  `customize_icons` stages the resolved icon at
  `<flutter_dir>/linux/app_icon.png` (installed by the runner's CMake as
  `data/app_icon.png`) and records the hicolor theme directory in
  `app_icon.cmake`. The `dart run flutter_launcher_icons` invocation is
  stubbed out.
* **The desktop entry** — `linux/{{cookiecutter.bundle_id}}.desktop`,
  installed into `share/applications/` so desktop environments resolve the
  launcher name and icon from it. `Exec` and `Categories` are escaped by
  `flet build`; every other value by the template.
"""

import argparse
import json
import os
import re
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional

import pytest
import yaml
from jinja2 import Environment, StrictUndefined

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
    Build the PNG signature and IHDR header that `get_png_size` reads.

    Args:
        width: Pixel width to encode.
        height: Pixel height to encode.

    Returns:
        Just enough of a PNG for the size reader; not a decodable image.
    """

    return (
        b"\x89PNG\r\n\x1a\n"
        + (13).to_bytes(4, "big")
        + b"IHDR"
        + width.to_bytes(4, "big")
        + height.to_bytes(4, "big")
    )


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
    cmd.verbose = 0
    cmd.dart_exe = "dart"
    cmd.emojis = {"checkmark": "", "loading": ""}
    cmd.options = SimpleNamespace(android_adaptive_icon_background=None)
    cmd.get_pyproject = lambda *_: None
    cmd.update_status = lambda *_: None
    cmd.run = lambda *a, **k: SimpleNamespace(returncode=0, stdout="", stderr="")
    cmd.customize_icons()
    return cmd


def _staged_icon(cmd: BaseBuildCommand) -> Path:
    """The path `customize_icons` stages the Linux icon to."""

    return cmd.flutter_dir / "linux" / "app_icon.png"


class TestLinuxIconStaging:
    """
    Which icon `customize_icons` stages for a Linux build, and when.

    The bundle must always end up with an icon it can show, whether the app
    supplies a Linux-specific one, a generic one, or none at all — and a
    non-Linux build must not pay for any of it.
    """

    def test_user_icon_staged_for_linux(self, tmp_path):
        """A generic `icon.png` is staged when no Linux-specific icon exists."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": b"user-icon"})
        assert _staged_icon(cmd).read_bytes() == b"user-icon"

    def test_icon_linux_beats_default_icon(self, tmp_path):
        """`icon_linux.png` wins over the generic `icon.png`."""
        cmd = _run_customize_icons(
            tmp_path,
            assets={"icon.png": b"generic", "icon_linux.png": b"linux-specific"},
        )
        assert _staged_icon(cmd).read_bytes() == b"linux-specific"

    def test_template_default_staged_without_assets(self, tmp_path):
        """An app with no `assets` dir still gets the template's default icon,
        so a Linux bundle is never built without a window icon."""
        cmd = _run_customize_icons(tmp_path, assets=None)
        assert _staged_icon(cmd).read_bytes() == _png_bytes()

    def test_template_default_staged_when_no_usable_icon(self, tmp_path):
        """An assets dir holding only an undecodable vector falls back too."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.svg": b"<svg/>"})
        assert _staged_icon(cmd).read_bytes() == _png_bytes()

    def test_missing_template_default_degrades_gracefully(self, tmp_path):
        """A custom build template that ships no `images/icon.png` produces an
        icon-less bundle rather than failing the build on the copy."""
        cmd = _run_customize_icons(tmp_path, assets=None, template_default_icon=False)
        assert not _staged_icon(cmd).exists()

    def test_not_staged_for_other_targets(self, tmp_path):
        """Non-Linux targets stage nothing; only their own generators run."""
        cmd = _run_customize_icons(
            tmp_path, assets={"icon.png": b"user-icon"}, target_platform="windows"
        )
        assert not _staged_icon(cmd).exists()

    def test_icon_linux_ignored_for_other_targets(self, tmp_path):
        """The `icon_linux` lookup is skipped entirely off Linux. It has no
        consumer there, and letting it run would copy a dead file and churn
        the icons hash, re-running the icon generator for nothing."""
        cmd = _run_customize_icons(
            tmp_path,
            assets={"icon_linux.png": b"linux-only"},
            target_platform="windows",
        )
        assert not (cmd.flutter_dir / "images" / "icon_linux.png").exists()

    def test_restaged_when_user_icon_changes(self, tmp_path):
        """Editing the source icon restages it rather than keeping the copy."""
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": b"first"})
        assert _staged_icon(cmd).read_bytes() == b"first"
        icon = cmd.package_app_path / "assets" / "icon.png"
        icon.write_bytes(b"second")
        # Change detection keys on mtime; bump it explicitly so the test does
        # not depend on filesystem timestamp granularity.
        stat = icon.stat()
        os.utime(icon, (stat.st_atime, stat.st_mtime + 10))
        cmd.customize_icons()
        assert _staged_icon(cmd).read_bytes() == b"second"

    def test_non_png_icon_warns_but_stages(self, tmp_path, capsys):
        """A non-PNG icon is still staged, but warns: it is bundled as-is, and a
        format with no GDK loader on the target system shows no icon at all."""
        cmd = _run_customize_icons(tmp_path, assets={"icon_linux.webp": b"webp-icon"})
        assert _staged_icon(cmd).read_bytes() == b"webp-icon"
        combined = capsys.readouterr()
        assert "icon_linux.webp" in (combined.out + combined.err)

    def test_256_png_stages_without_warning(self, tmp_path, capsys):
        """The recommended 256x256 PNG stages silently."""
        cmd = _run_customize_icons(tmp_path, assets={"icon_linux.png": _png_bytes()})
        assert _staged_icon(cmd).exists()
        combined = capsys.readouterr()
        assert "Warning" not in (combined.out + combined.err)


class TestIconThemeSize:
    """
    The hicolor directory the themed icon is installed into.

    Only sizes hicolor's `index.theme` declares are ever scanned, so naming a
    directory hicolor does not know is worse than falling back: the icon is
    installed and then never found.
    """

    @staticmethod
    def _theme_size(cmd: BaseBuildCommand) -> str:
        """The generated CMake fragment that carries the resolved size."""
        return (cmd.flutter_dir / "linux" / "app_icon.cmake").read_text()

    def test_theme_size_matches_icon(self, tmp_path):
        """A size hicolor declares is used as-is, not flattened to 256x256."""
        cmd = _run_customize_icons(
            tmp_path, assets={"icon_linux.png": _png_bytes(512, 512)}
        )
        assert 'set(FLET_APP_ICON_THEME_SIZE "512x512")' in self._theme_size(cmd)

    def test_theme_size_falls_back_for_unusual_icons(self, tmp_path):
        """A non-hicolor size and a non-square icon both fall back."""
        cmd = _run_customize_icons(
            tmp_path, assets={"icon_linux.png": _png_bytes(1024, 1024)}
        )
        assert 'set(FLET_APP_ICON_THEME_SIZE "256x256")' in self._theme_size(cmd)
        cmd = _run_customize_icons(
            tmp_path / "b", assets={"icon_linux.png": _png_bytes(256, 128)}
        )
        assert 'set(FLET_APP_ICON_THEME_SIZE "256x256")' in self._theme_size(cmd)

    def test_resolve_icon_theme_size(self):
        """Only sizes declared by hicolor's `index.theme` are used directly."""
        resolve = BaseBuildCommand.resolve_icon_theme_size
        assert resolve((48, 48)) == "48x48"
        assert resolve((256, 256)) == "256x256"
        assert resolve((512, 512)) == "512x512"
        # Unknown size (unreadable or non-PNG), non-square, and sizes outside
        # the theme's set.
        assert resolve(None) == "256x256"
        assert resolve((500, 500)) == "256x256"
        assert resolve((1024, 1024)) == "256x256"
        assert resolve((512, 256)) == "256x256"
        for undeclared in (28, 42, 160, 384):
            assert resolve((undeclared, undeclared)) == "256x256"

    def test_png_size_reads_ihdr(self, tmp_path):
        """Sizes come from the PNG header; anything unreadable is `None`."""
        icon = tmp_path / "icon.png"
        icon.write_bytes(_png_bytes(width=512, height=384))
        assert BaseBuildCommand.get_png_size(icon) == (512, 384)
        not_png = tmp_path / "not_png.png"
        not_png.write_bytes(b"actually-jpeg-bytes")
        assert BaseBuildCommand.get_png_size(not_png) is None
        assert BaseBuildCommand.get_png_size(tmp_path / "missing.png") is None


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
    """Rendering of `linux/{{cookiecutter.bundle_id}}.desktop`."""

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


class TestBuildTemplateContract:
    """
    Invariants of the build template itself, independent of any one platform.

    Both bugs these cover shipped at least once: a context key the templates
    read but `cookiecutter.json` never declared (cookiecutter drops it, so the
    value silently vanished), and a template that stopped being parseable
    while unrendered, which breaks the CI step that patches it in place.
    """

    @staticmethod
    def _declared_keys() -> set:
        """The context keys `cookiecutter.json` declares."""
        with open(BUILD_TEMPLATE_DIR.parent / "cookiecutter.json") as f:
            return set(json.load(f))

    @staticmethod
    def _referenced_keys() -> dict:
        """Every `cookiecutter.<key>` referenced by a template, by file."""
        found = {}
        for path in BUILD_TEMPLATE_DIR.rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text()
            except UnicodeDecodeError:
                continue  # binary asset, e.g. images/icon.png
            # The negative lookahead skips method calls such as
            # `cookiecutter.items()` in .vars, which are not context keys.
            for key in re.findall(
                r"cookiecutter\.([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*\()", text
            ):
                found.setdefault(key, set()).add(path.name)
        return found

    def test_every_referenced_key_is_declared(self):
        """
        A key a template reads but `cookiecutter.json` omits is dropped from
        the context, so the template silently renders it empty — which is how
        `--description` reached nothing for as long as it did.
        """
        declared = self._declared_keys()
        undeclared = {
            key: sorted(files)
            for key, files in self._referenced_keys().items()
            if key not in declared
        }
        assert not undeclared, f"referenced but not declared: {undeclared}"

    def test_pubspec_parses_while_unrendered(self):
        """
        `.github/scripts/patch_pubspec_version.py` loads this file as YAML
        before cookiecutter ever runs, so an unquoted `{{` — which YAML reads
        as a flow mapping — fails the release build.
        """
        with open(TEMPLATE_PUBSPEC) as f:
            assert yaml.safe_load(f), "template pubspec.yaml must parse as YAML"

    @pytest.mark.parametrize(
        "description",
        ["plain", "Bob's tool", 'has "quotes"', "back\\slash", "multi\nline\ttab"],
    )
    def test_rendered_pubspec_is_valid_yaml(self, description):
        """A description of any shape must still render a parseable pubspec."""
        rendered = _render_template(
            TEMPLATE_PUBSPEC,
            project_name="test_app",
            pubspec_description=BaseBuildCommand.escape_single_quoted_yaml(description),
        )
        parsed = yaml.safe_load(rendered)
        assert parsed["description"] == re.sub(r"[\x00-\x1f]", " ", description)
