"""
Flutter SDK architecture handling for `flet build windows` on Windows on ARM.

Flet's Python runtime for Windows is x64-only, so an ARM64 Flutter SDK, which
builds ARM64 Windows apps, must not be used for a Windows build. The SDK's
architecture comes from `dart --version`, which is stubbed here, so no Flutter
SDK is needed.
"""

import argparse
import os
from types import SimpleNamespace

import pytest
from packaging import version

from flet_cli.commands.build import Command
from flet_cli.utils.flutter import get_flutter_dir

FLUTTER_VERSION = "3.44.8"
EXTERNAL_FLUTTER_EXE = os.path.join(os.sep + "opt", "flutter", "bin", "flutter")
# `dart --version` output, formatted with the `<os>_<arch>` Dart runs on.
DART_VERSION = (
    'Dart SDK version: 3.12.2 (stable) (Tue Jun 9 01:11:39 2026 -0700) on "{}"\n'
)


class Exit(Exception):
    """Captures `cleanup(1, message)` calls, which normally sys.exit."""

    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"cleanup({code}): {message}")


def make_command(**attrs) -> Command:
    """
    Build a `flet build windows` command on Windows without parsing a command line.

    Args:
        attrs: Attributes to set on the command, overriding the defaults.

    Returns:
        A command whose `cleanup` raises `Exit` instead of exiting.
    """

    cmd = Command(argparse.ArgumentParser())
    cmd.required_flutter_version = version.Version(FLUTTER_VERSION)
    cmd.current_platform = "Windows"
    cmd.package_platform = "Windows"
    cmd.target_platform = "windows"

    def cleanup(code, message=None, **kwargs):
        raise Exit(code, message)

    cmd.cleanup = cleanup
    for name, value in attrs.items():
        setattr(cmd, name, value)
    return cmd


def dart_version_runner(stdout="", stderr=""):
    """
    Return a stub for `run()` answering `dart --version`, recording its calls.

    Args:
        stdout: Standard output of the stubbed `dart --version`.
        stderr: Standard error of the stubbed `dart --version`.

    Returns:
        A `run()` replacement whose `calls` lists the arguments of each call.
    """

    def run(args, cwd, env=None, capture_output=True):
        run.calls.append(args)
        return SimpleNamespace(returncode=0, stdout=stdout, stderr=stderr)

    run.calls = []
    return run


def unexpected_dart_call():
    """Fail the test if the SDK architecture is queried."""
    raise AssertionError("`dart --version` must not run")


class TestFlutterArch:
    """How `flutter_arch()` reads the SDK architecture from `dart --version`."""

    @pytest.mark.parametrize(
        ("stdout", "stderr", "expected"),
        [
            (DART_VERSION.format("windows_arm64"), "", "arm64"),
            (DART_VERSION.format("windows_x64"), "", "x64"),
            ("", DART_VERSION.format("windows_arm64"), "arm64"),
        ],
        ids=["windows_arm64", "windows_x64", "on-stderr"],
    )
    def test_parses_dart_version(self, stdout, stderr, expected):
        """The architecture suffix of the `on "<os>_<arch>"` part is returned."""
        cmd = make_command(dart_exe="dart", run=dart_version_runner(stdout, stderr))

        assert cmd.flutter_arch() == expected

    def test_unparsable_output_is_none(self):
        """Output without an `on "<os>_<arch>"` part gives `None`."""
        cmd = make_command(
            dart_exe="dart", run=dart_version_runner("Dart SDK version: 3.12.2\n")
        )

        assert cmd.flutter_arch() is None

    def test_cached_per_dart_executable(self):
        """Dart runs once per executable, so switching SDKs reads the new one."""
        cmd = make_command(
            dart_exe="arm64-dart",
            run=dart_version_runner(DART_VERSION.format("windows_arm64")),
        )
        assert cmd.flutter_arch() == "arm64"
        assert cmd.flutter_arch() == "arm64"
        assert len(cmd.run.calls) == 1

        cmd.dart_exe = "x64-dart"
        cmd.run = dart_version_runner(DART_VERSION.format("windows_x64"))
        assert cmd.flutter_arch() == "x64"


class TestFlutterSdkSupported:
    """Which Flutter SDKs `flet build` accepts, by host, target and architecture."""

    @pytest.mark.parametrize(
        "flutter_exe",
        [
            EXTERNAL_FLUTTER_EXE,
            os.path.join(
                get_flutter_dir(FLUTTER_VERSION) + "-custom", "bin", "flutter"
            ),
        ],
        ids=["outside-home", "sibling-of-managed-dir"],
    )
    def test_external_arm64_sdk_is_replaced(self, flutter_exe):
        """An ARM64 SDK outside Flet's own directory is swapped for Flet's x64 SDK."""
        cmd = make_command(flutter_exe=flutter_exe, flutter_arch=lambda: "arm64")

        assert cmd.flutter_sdk_supported() is False

    def test_managed_arm64_sdk_fails(self):
        """An ARM64 SDK in Flet's own directory fails, asking to delete it."""
        cmd = make_command(
            flutter_exe=os.path.join(
                get_flutter_dir(FLUTTER_VERSION), "bin", "flutter.bat"
            ),
            flutter_arch=lambda: "arm64",
            skip_flutter_doctor=False,
        )

        with pytest.raises(Exit) as exc_info:
            cmd.flutter_sdk_supported()

        assert exc_info.value.code == 1
        assert "Delete that directory" in exc_info.value.message

    def test_x64_sdk_is_supported(self):
        """An x64 SDK builds Windows apps on any Windows host."""
        cmd = make_command(flutter_exe=EXTERNAL_FLUTTER_EXE, flutter_arch=lambda: "x64")

        assert cmd.flutter_sdk_supported() is True

    @pytest.mark.parametrize(
        ("host", "package_platform"),
        [
            ("Windows", "Android"),
            ("Darwin", "Darwin"),
            ("Linux", "Linux"),
            ("Darwin", "Windows"),
            ("Linux", "Windows"),
        ],
        ids=[
            "android-on-windows",
            "macos-on-macos",
            "linux-on-linux",
            "windows-on-macos",
            "windows-on-linux",
        ],
    )
    def test_other_builds_are_supported_without_running_dart(
        self, host, package_platform
    ):
        """Builds other than Windows-on-Windows accept any SDK without asking Dart."""
        cmd = make_command(
            current_platform=host,
            package_platform=package_platform,
            flutter_exe=EXTERNAL_FLUTTER_EXE,
            flutter_arch=unexpected_dart_call,
        )

        assert cmd.flutter_sdk_supported() is True


class TestWindowsBuildOutput:
    """Where `flet build windows` looks for the app Flutter built."""

    @pytest.mark.parametrize(
        ("sdk_arch", "host_machine", "expected"),
        [
            ("x64", "ARM64", "x64"),
            ("arm64", "AMD64", "arm64"),
            (None, "AMD64", "x64"),
        ],
        ids=["x64-sdk-on-arm64", "arm64-sdk", "unknown-sdk-arch"],
    )
    def test_output_follows_sdk_arch(
        self, tmp_path, monkeypatch, sdk_arch, host_machine, expected
    ):
        """The output directory follows the SDK's architecture, not the host's."""
        monkeypatch.setattr("platform.machine", lambda: host_machine)
        cmd = make_command(
            flutter_dir=tmp_path,
            template_data={
                "artifact_name": "app",
                "project_name": "app",
                "product_name": "app",
            },
            flutter_arch=lambda: sdk_arch,
        )

        (output,) = cmd.platforms["windows"]["outputs"]
        assert cmd.resolve_output_path(output) == str(
            tmp_path / "build" / "windows" / expected / "runner" / "Release" / "*"
        )
