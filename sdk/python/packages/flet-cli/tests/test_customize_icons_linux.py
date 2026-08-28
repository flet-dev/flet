"""Linux icon staging in `flet build` (issue #2269).

`flutter_launcher_icons` has no Linux generator, so `customize_icons` must
stage the resolved icon at a fixed path (`<flutter_dir>/linux/app_icon.png`)
that the Linux runner's CMake installs into the bundle as
`data/app_icon.png`. These tests drive `customize_icons` end to end with the
external `dart run flutter_launcher_icons` invocation stubbed out.
"""

from types import SimpleNamespace

import yaml

from flet_cli.commands.build_base import BaseBuildCommand


def _run_customize_icons(tmp_path, *, assets=None, target_platform="linux"):
    """
    Drive `BaseBuildCommand.customize_icons` against a faked project layout.

    Args:
        tmp_path: pytest tmp dir.
        assets: mapping of file name to content for the user's `assets` dir,
            or `None` for an app without an assets dir.
        target_platform: `flet build` target platform.

    Returns:
        The faked command object (with `flutter_dir` etc. set).
    """
    app_path = tmp_path / "app"
    app_path.mkdir()
    if assets is not None:
        assets_dir = app_path / "assets"
        assets_dir.mkdir()
        for name, content in assets.items():
            (assets_dir / name).write_bytes(content)

    flutter_dir = tmp_path / "flutter"
    (flutter_dir / "images").mkdir(parents=True)
    (flutter_dir / "images" / "icon.png").write_bytes(b"template-default")
    (flutter_dir / "linux").mkdir()

    build_dir = tmp_path / "build"
    build_dir.mkdir()

    pubspec_path = flutter_dir / "pubspec.yaml"
    # Mirrors the platform keys of the build template's pubspec.yaml, which
    # fallback_image expects to exist.
    pubspec = {
        "flutter_launcher_icons": {
            "image_path": "images/icon.png",
            "web": {"generate": True},
            "windows": {"generate": True},
            "macos": {"generate": True},
        }
    }
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


def _staged_icon(cmd):
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
    assert _staged_icon(cmd).read_bytes() == b"template-default"


def test_template_default_staged_when_no_usable_icon(tmp_path):
    # An assets dir exists, but its only icon is an undecodable vector.
    cmd = _run_customize_icons(tmp_path, assets={"icon.svg": b"<svg/>"})
    assert _staged_icon(cmd).read_bytes() == b"template-default"


def test_not_staged_for_other_targets(tmp_path):
    cmd = _run_customize_icons(
        tmp_path, assets={"icon.png": b"user-icon"}, target_platform="windows"
    )
    assert not _staged_icon(cmd).exists()


def test_non_png_icon_warns_but_stages(tmp_path, capsys):
    cmd = _run_customize_icons(tmp_path, assets={"icon_linux.webp": b"webp-icon"})
    assert _staged_icon(cmd).read_bytes() == b"webp-icon"
    combined = capsys.readouterr()
    assert "icon_linux.webp" in (combined.out + combined.err)


def test_restaged_when_user_icon_changes(tmp_path):
    # HashStamp change detection: a re-run with a modified user icon must
    # overwrite the previously staged copy.
    cmd = _run_customize_icons(tmp_path, assets={"icon.png": b"first"})
    assert _staged_icon(cmd).read_bytes() == b"first"
    icon = cmd.package_app_path / "assets" / "icon.png"
    icon.write_bytes(b"second")
    cmd.customize_icons()
    assert _staged_icon(cmd).read_bytes() == b"second"
