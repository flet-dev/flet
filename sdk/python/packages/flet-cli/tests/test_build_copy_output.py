"""How `flet build` copies Flutter's build output into the output directory."""

import argparse
from pathlib import Path

import pytest

from flet_cli.commands.build_base import BaseBuildCommand

WINDOWS_RELEASE = "build/windows/x64/runner/Release"
MACOS_RELEASE = "build/macos/Build/Products/Release"


def _command(
    tmp_path: Path, target_platform: str, artifact_name: str = "MyApp"
) -> BaseBuildCommand:
    """
    Build a command that copies from `tmp_path/flutter` into `tmp_path/out`.

    Args:
        tmp_path: pytest tmp dir.
        target_platform: Key of `BaseBuildCommand.platforms`.
        artifact_name: Value substituted for `{artifact_name}` in outputs.

    Returns:
        A command whose `cleanup` raises `SystemExit` with the exit code and
            records the message in `cleanup_messages`.
    """

    cmd = BaseBuildCommand(argparse.ArgumentParser())
    cmd.options = argparse.Namespace()
    cmd.verbose = 0
    cmd.flutter_dir = tmp_path / "flutter"
    cmd.out_dir = tmp_path / "out"
    cmd.rel_out_dir = "out"
    cmd.assets_path = tmp_path / "assets"
    cmd.target_platform = target_platform
    cmd.package_platform = cmd.platforms[target_platform]["package_platform"]
    cmd.template_data = {
        "artifact_name": artifact_name,
        "project_name": "my_app",
        "product_name": "My App",
    }
    cmd.emojis = {"checkmark": ""}
    cmd.update_status = lambda *_: None
    cmd.flutter_arch = lambda: "x64"
    cmd.cleanup_messages = []

    def cleanup(exit_code, message=None, no_border=False):
        cmd.cleanup_messages.append(message)
        raise SystemExit(exit_code)

    cmd.cleanup = cleanup
    return cmd


def test_windows_release_contents_are_copied(tmp_path):
    """Every entry of the Windows `Release` directory lands in the output dir."""
    release = tmp_path / "flutter" / WINDOWS_RELEASE
    (release / "data").mkdir(parents=True)
    (release / "my_app.exe").write_text("exe")
    cmd = _command(tmp_path, "windows")

    cmd.copy_build_output()

    assert sorted(p.name for p in cmd.out_dir.iterdir()) == ["data", "my_app.exe"]


def test_macos_copies_only_the_app_bundle(tmp_path):
    """Only `{artifact_name}.app` is copied out of the macOS `Release` directory."""
    release = tmp_path / "flutter" / MACOS_RELEASE
    (release / "MyApp.app" / "Contents").mkdir(parents=True)
    (release / "FlutterMacOS.framework").mkdir()
    cmd = _command(tmp_path, "macos")

    cmd.copy_build_output()

    assert [p.name for p in cmd.out_dir.iterdir()] == ["MyApp.app"]


def test_macos_app_name_is_matched_literally(tmp_path):
    """An artifact name with glob characters still matches its `.app` bundle."""
    release = tmp_path / "flutter" / MACOS_RELEASE
    (release / "My App [Beta].app" / "Contents").mkdir(parents=True)
    cmd = _command(tmp_path, "macos", artifact_name="My App [Beta]")

    cmd.copy_build_output()

    assert [p.name for p in cmd.out_dir.iterdir()] == ["My App [Beta].app"]


@pytest.mark.parametrize(
    ("target_platform", "make_tree"),
    [
        pytest.param("windows", lambda f: None, id="windows-no-release-dir"),
        pytest.param(
            "windows",
            lambda f: (f / WINDOWS_RELEASE).mkdir(parents=True),
            id="windows-empty-release-dir",
        ),
        pytest.param(
            "macos",
            lambda f: (f / MACOS_RELEASE / "Other.app").mkdir(parents=True),
            id="macos-release-dir-without-app",
        ),
    ],
)
def test_missing_build_output_fails(tmp_path, target_platform, make_tree):
    """The build fails, naming the searched path, when no output matches."""
    make_tree(tmp_path / "flutter")
    cmd = _command(tmp_path, target_platform)

    with pytest.raises(SystemExit) as exc_info:
        cmd.copy_build_output()

    assert exc_info.value.code == 1
    assert "Build output not found in" in cmd.cleanup_messages[-1]
    assert not cmd.out_dir.exists()
