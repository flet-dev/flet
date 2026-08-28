"""Linux icon staging in `flet build` (issue #2269).

`flutter_launcher_icons` has no Linux generator, so `customize_icons` must
stage the resolved icon at a fixed path (`<flutter_dir>/linux/app_icon.png`)
that the Linux runner's CMake installs into the bundle as
`data/app_icon.png`. These tests drive `customize_icons` end to end with the
external `dart run flutter_launcher_icons` invocation stubbed out.
"""

import os
from pathlib import Path
from types import SimpleNamespace
from typing import Optional

import yaml
from jinja2 import Environment

from flet_cli.commands.build_base import BaseBuildCommand

TEMPLATE_PUBSPEC = (
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
    / "pubspec.yaml"
)


def _template_pubspec() -> dict:
    """Render the real build-template pubspec the way cookiecutter would."""
    rendered = (
        Environment()
        .from_string(TEMPLATE_PUBSPEC.read_text())
        .render(cookiecutter={"project_name": "test_app", "project_description": ""})
    )
    return yaml.safe_load(rendered)


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
    app_path.mkdir(exist_ok=True)
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
    pubspec = _template_pubspec()
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


def test_user_icon_staged_for_linux(tmp_path):
    cmd = _run_customize_icons(tmp_path, assets={"icon.png": b"user-icon"})
    assert _staged_icon(cmd).read_bytes() == b"user-icon"


def test_icon_linux_beats_default_icon(tmp_path):
    cmd = _run_customize_icons(
        tmp_path,
        assets={"icon.png": b"generic", "icon_linux.png": b"linux-specific"},
    )
    assert _staged_icon(cmd).read_bytes() == b"linux-specific"


def test_template_default_staged_without_assets(tmp_path):
    # No assets dir at all: the template's default icon must still be staged
    # so the Linux bundle always ships a window icon.
    cmd = _run_customize_icons(tmp_path, assets=None)
    assert _staged_icon(cmd).read_bytes() == _png_bytes()


def test_template_default_staged_when_no_usable_icon(tmp_path):
    # An assets dir exists, but its only icon is an undecodable vector.
    cmd = _run_customize_icons(tmp_path, assets={"icon.svg": b"<svg/>"})
    assert _staged_icon(cmd).read_bytes() == _png_bytes()


def test_missing_template_default_degrades_gracefully(tmp_path):
    # A custom build template without images/icon.png must not crash the
    # build; the bundle simply ships without an icon.
    cmd = _run_customize_icons(tmp_path, assets=None, template_default_icon=False)
    assert not _staged_icon(cmd).exists()


def test_not_staged_for_other_targets(tmp_path):
    cmd = _run_customize_icons(
        tmp_path, assets={"icon.png": b"user-icon"}, target_platform="windows"
    )
    assert not _staged_icon(cmd).exists()


def test_icon_linux_ignored_for_other_targets(tmp_path):
    # The icon_linux lookup must not run (copy files, feed the hash) on
    # non-linux builds — it has no consumer there.
    cmd = _run_customize_icons(
        tmp_path, assets={"icon_linux.png": b"linux-only"}, target_platform="windows"
    )
    assert not (cmd.flutter_dir / "images" / "icon_linux.png").exists()


def test_non_png_icon_warns_but_stages(tmp_path, capsys):
    cmd = _run_customize_icons(tmp_path, assets={"icon_linux.webp": b"webp-icon"})
    assert _staged_icon(cmd).read_bytes() == b"webp-icon"
    combined = capsys.readouterr()
    assert "icon_linux.webp" in (combined.out + combined.err)


def test_wrong_size_png_warns_but_stages(tmp_path, capsys):
    # The icon lands in the 256x256 hicolor directory, so other sizes get a
    # build-time warning.
    icon = _png_bytes(width=1024, height=1024)
    cmd = _run_customize_icons(tmp_path, assets={"icon_linux.png": icon})
    assert _staged_icon(cmd).read_bytes() == icon
    combined = capsys.readouterr()
    assert "1024" in (combined.out + combined.err)


def test_256_png_stages_without_warning(tmp_path, capsys):
    cmd = _run_customize_icons(tmp_path, assets={"icon_linux.png": _png_bytes()})
    assert _staged_icon(cmd).exists()
    combined = capsys.readouterr()
    assert "Warning" not in (combined.out + combined.err)


def test_restaged_when_user_icon_changes(tmp_path):
    # HashStamp change detection: a re-run with a modified user icon must
    # overwrite the previously staged copy.
    cmd = _run_customize_icons(tmp_path, assets={"icon.png": b"first"})
    assert _staged_icon(cmd).read_bytes() == b"first"
    icon = cmd.package_app_path / "assets" / "icon.png"
    icon.write_bytes(b"second")
    # Change detection keys on mtime; bump it explicitly so the test doesn't
    # depend on filesystem timestamp granularity.
    stat = icon.stat()
    os.utime(icon, (stat.st_atime, stat.st_mtime + 10))
    cmd.customize_icons()
    assert _staged_icon(cmd).read_bytes() == b"second"


def test_png_size_reads_ihdr(tmp_path):
    icon = tmp_path / "icon.png"
    icon.write_bytes(_png_bytes(width=512, height=384))
    assert BaseBuildCommand.get_png_size(icon) == (512, 384)
    not_png = tmp_path / "not_png.png"
    not_png.write_bytes(b"actually-jpeg-bytes")
    assert BaseBuildCommand.get_png_size(not_png) is None
    assert BaseBuildCommand.get_png_size(tmp_path / "missing.png") is None
