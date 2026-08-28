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

import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional

import pytest
import yaml
from jinja2 import Environment

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
    """Render a build-template file the way cookiecutter would."""
    env = Environment(keep_trailing_newline=True)
    return env.from_string(path.read_text()).render(cookiecutter=context)


def _png_bytes(width: int = 256, height: int = 256) -> bytes:
    """Build the PNG signature + IHDR header `get_png_size` reads."""
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
        template_default_icon: whether the (rendered) Flutter project ships
            the template's default `images/icon.png`.

    Returns:
        The faked command object (with `flutter_dir` etc. set).
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
            TEMPLATE_PUBSPEC, project_name="test_app", project_description=""
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
    return cmd.flutter_dir / "linux" / "app_icon.png"


class TestLinuxIconStaging:
    """Which icon `customize_icons` stages for a Linux build, and when."""

    def test_user_icon_staged_for_linux(self, tmp_path):
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": b"user-icon"})
        assert _staged_icon(cmd).read_bytes() == b"user-icon"

    def test_icon_linux_beats_default_icon(self, tmp_path):
        cmd = _run_customize_icons(
            tmp_path,
            assets={"icon.png": b"generic", "icon_linux.png": b"linux-specific"},
        )
        assert _staged_icon(cmd).read_bytes() == b"linux-specific"

    def test_template_default_staged_without_assets(self, tmp_path):
        # No assets dir at all: the template's default icon must still be
        # staged so the Linux bundle always ships a window icon.
        cmd = _run_customize_icons(tmp_path, assets=None)
        assert _staged_icon(cmd).read_bytes() == _png_bytes()

    def test_template_default_staged_when_no_usable_icon(self, tmp_path):
        # An assets dir exists, but its only icon is an undecodable vector.
        cmd = _run_customize_icons(tmp_path, assets={"icon.svg": b"<svg/>"})
        assert _staged_icon(cmd).read_bytes() == _png_bytes()

    def test_missing_template_default_degrades_gracefully(self, tmp_path):
        # A custom build template without images/icon.png must not crash the
        # build; the bundle simply ships without an icon.
        cmd = _run_customize_icons(tmp_path, assets=None, template_default_icon=False)
        assert not _staged_icon(cmd).exists()

    def test_not_staged_for_other_targets(self, tmp_path):
        cmd = _run_customize_icons(
            tmp_path, assets={"icon.png": b"user-icon"}, target_platform="windows"
        )
        assert not _staged_icon(cmd).exists()

    def test_icon_linux_ignored_for_other_targets(self, tmp_path):
        # The icon_linux lookup must not run (copy files, feed the hash) on
        # non-linux builds — it has no consumer there.
        cmd = _run_customize_icons(
            tmp_path,
            assets={"icon_linux.png": b"linux-only"},
            target_platform="windows",
        )
        assert not (cmd.flutter_dir / "images" / "icon_linux.png").exists()

    def test_restaged_when_user_icon_changes(self, tmp_path):
        # HashStamp change detection: a re-run with a modified user icon must
        # overwrite the previously staged copy.
        cmd = _run_customize_icons(tmp_path, assets={"icon.png": b"first"})
        assert _staged_icon(cmd).read_bytes() == b"first"
        icon = cmd.package_app_path / "assets" / "icon.png"
        icon.write_bytes(b"second")
        # Change detection keys on mtime; bump it explicitly so the test
        # doesn't depend on filesystem timestamp granularity.
        stat = icon.stat()
        os.utime(icon, (stat.st_atime, stat.st_mtime + 10))
        cmd.customize_icons()
        assert _staged_icon(cmd).read_bytes() == b"second"

    def test_non_png_icon_warns_but_stages(self, tmp_path, capsys):
        cmd = _run_customize_icons(tmp_path, assets={"icon_linux.webp": b"webp-icon"})
        assert _staged_icon(cmd).read_bytes() == b"webp-icon"
        combined = capsys.readouterr()
        assert "icon_linux.webp" in (combined.out + combined.err)

    def test_256_png_stages_without_warning(self, tmp_path, capsys):
        cmd = _run_customize_icons(tmp_path, assets={"icon_linux.png": _png_bytes()})
        assert _staged_icon(cmd).exists()
        combined = capsys.readouterr()
        assert "Warning" not in (combined.out + combined.err)


class TestIconThemeSize:
    """The hicolor directory the themed icon is installed into."""

    @staticmethod
    def _theme_size(cmd: BaseBuildCommand) -> str:
        return (cmd.flutter_dir / "linux" / "app_icon.cmake").read_text()

    def test_theme_size_matches_icon(self, tmp_path):
        # A standard hicolor size must be declared as itself, not as 256x256.
        cmd = _run_customize_icons(
            tmp_path, assets={"icon_linux.png": _png_bytes(512, 512)}
        )
        assert 'set(FLET_APP_ICON_THEME_SIZE "512x512")' in self._theme_size(cmd)

    def test_theme_size_falls_back_for_unusual_icons(self, tmp_path):
        # 1024x1024 is not a hicolor theme directory, and neither is a
        # non-square icon — both fall back to the scalable-from 256x256 dir.
        cmd = _run_customize_icons(
            tmp_path, assets={"icon_linux.png": _png_bytes(1024, 1024)}
        )
        assert 'set(FLET_APP_ICON_THEME_SIZE "256x256")' in self._theme_size(cmd)
        cmd = _run_customize_icons(
            tmp_path / "b", assets={"icon_linux.png": _png_bytes(256, 128)}
        )
        assert 'set(FLET_APP_ICON_THEME_SIZE "256x256")' in self._theme_size(cmd)

    def test_resolve_icon_theme_size(self):
        resolve = BaseBuildCommand.resolve_icon_theme_size
        assert resolve((48, 48)) == "48x48"
        assert resolve((256, 256)) == "256x256"
        assert resolve((512, 512)) == "512x512"
        # Unknown size (unreadable/non-PNG), non-square, and non-hicolor sizes.
        assert resolve(None) == "256x256"
        assert resolve((500, 500)) == "256x256"
        assert resolve((1024, 1024)) == "256x256"
        assert resolve((512, 256)) == "256x256"
        # Not declared by hicolor's index.theme: an icon installed into one of
        # these directories is never scanned, so it must fall back.
        for undeclared in (28, 42, 160, 384):
            assert resolve((undeclared, undeclared)) == "256x256"

    def test_png_size_reads_ihdr(self, tmp_path):
        icon = tmp_path / "icon.png"
        icon.write_bytes(_png_bytes(width=512, height=384))
        assert BaseBuildCommand.get_png_size(icon) == (512, 384)
        not_png = tmp_path / "not_png.png"
        not_png.write_bytes(b"actually-jpeg-bytes")
        assert BaseBuildCommand.get_png_size(not_png) is None
        assert BaseBuildCommand.get_png_size(tmp_path / "missing.png") is None


class TestDesktopEntryEscaping:
    """`Exec` and `Categories`, which `flet build` escapes before rendering."""

    @pytest.mark.parametrize(
        ("raw", "expected"),
        [
            ("my_app", "my_app"),
            ("my app", "my app"),
            # " ` $ \ are reserved inside the quoted Exec value; each gets a
            # backslash, and every backslash is then doubled for the entry file.
            ('mid"dle', 'mid\\\\"dle'),
            ("my$app", "my\\\\$app"),
            ("a\\b", "a\\\\\\\\b"),
            ("tick`s", "tick\\\\`s"),
        ],
    )
    def test_escape_desktop_exec(self, raw, expected):
        assert BaseBuildCommand.escape_desktop_exec(raw) == expected

    def test_escape_desktop_categories(self):
        escape = BaseBuildCommand.escape_desktop_categories
        assert escape(["Game", "Education"]) == "Game;Education;"
        assert escape("Development") == "Development;"
        # A literal semicolon would split one category into two.
        assert escape(["Ut;ility"]) == "Ut\\;ility;"
        assert escape(["back\\slash"]) == "back\\\\slash;"
        # Blanks are dropped, and an all-blank list keeps the default.
        assert escape(["Game", "  ", ""]) == "Game;"
        assert escape([]) == "Utility;"

    @pytest.mark.parametrize("bad", [5, None, ["ok", 7], {"a": 1}])
    def test_escape_desktop_categories_rejects_non_strings(self, bad):
        # A bad pyproject value must surface as a clear error rather than a
        # jinja TypeError that wipes the build directory.
        with pytest.raises(ValueError):
            BaseBuildCommand.escape_desktop_categories(bad)


class TestDesktopEntryTemplate:
    """Rendering of `linux/{{cookiecutter.bundle_id}}.desktop`."""

    @staticmethod
    def _render(**overrides: str) -> str:
        context = {
            "product_name": "My App",
            "project_description": "",
            "desktop_exec": "my_app",
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
        "[Desktop Entry]" but leaves every key outside any group, and the whole
        file is then ignored.
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
        content = self._render()
        assert "\n[Desktop Entry]\n" in content, content[:400]

    def test_desktop_entry_fields(self):
        entry = self._parse(self._render(project_description="Does great things."))
        assert entry["Type"] == "Application"
        assert entry["Name"] == "My App"
        assert entry["Comment"] == "Does great things."
        assert entry["Exec"] == '"my_app" %U'
        assert entry["Icon"] == "com.example.my_app"
        assert entry["StartupWMClass"] == "com.example.my_app"
        assert entry["Categories"] == "Utility;"

    def test_no_unrendered_jinja(self):
        content = self._render(project_description="Does great things.")
        assert "{{" not in content and "{%" not in content

    def test_comment_omitted_without_description(self):
        content = self._render(project_description="")
        assert "Comment=" not in content
        # The conditional must not leave a blank line behind.
        assert 'Name=My App\nExec="my_app" %U' in content

    def test_multiline_description_flattened(self):
        # A newline inside Comment= would make the entry fail
        # desktop-file-validate and get ignored by the desktop environment.
        content = self._render(project_description="Line one.\nLine two.")
        assert "Comment=Line one. Line two." in content

    def test_control_characters_flattened_in_name_and_comment(self):
        content = self._render(
            product_name="My\tApp\nName", project_description="Tabbed\tdescription"
        )
        assert "Name=My App Name" in content
        assert "Comment=Tabbed description" in content

    def test_backslashes_escaped(self):
        # Desktop entry values use backslash escape sequences, so a literal
        # backslash must be doubled.
        content = self._render(project_description=r"Uses C:\path\now")
        assert r"Comment=Uses C:\\path\\now" in content

    def test_prepared_values_are_interpolated_verbatim(self):
        # Exec and Categories arrive already escaped; the template must not
        # escape them a second time.
        content = self._render(
            desktop_exec=r"weird\\\"name", linux_categories="Game;Fun;"
        )
        assert 'Exec="weird\\\\\\"name" %U' in content
        assert "Categories=Game;Fun;" in content
