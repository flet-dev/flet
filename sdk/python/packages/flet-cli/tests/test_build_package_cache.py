"""Dependency cache recovery when build artifacts have been removed."""

from types import SimpleNamespace

import pytest

from flet_cli.commands.build_base import BaseBuildCommand


@pytest.fixture
def command(tmp_path):
    cmd = BaseBuildCommand.__new__(BaseBuildCommand)
    cmd.build_dir = tmp_path / "build"
    cmd.flutter_dir = cmd.build_dir / "flutter"
    cmd.template_data = {"options": {"target_arch": []}}
    cmd.python_release = SimpleNamespace(android_abis=("arm64-v8a", "x86_64"))
    return cmd


def write_package(directory):
    package = directory / "flet" / "__init__.pyc"
    package.parent.mkdir(parents=True, exist_ok=True)
    package.write_bytes(b"package")


@pytest.mark.parametrize("platform", ["Windows", "Linux", "Darwin", "Emscripten"])
def test_missing_empty_and_populated_package_directory(command, platform):
    command.package_platform = platform
    root = command.flutter_dir if platform == "Emscripten" else command.build_dir
    packages = root / "site-packages"
    if platform == "Emscripten":
        packages = root / "build" / "site-packages"
        # A native cache must not mask missing web packages.
        write_package(command.build_dir / "site-packages")
    assert command._site_packages_missing()

    (packages / "flet").mkdir(parents=True)
    assert command._site_packages_missing()

    write_package(packages)
    assert not command._site_packages_missing()


def test_darwin_pod_metadata_is_not_a_package(command, tmp_path):
    command.package_platform = "Darwin"
    packages = command.build_dir / "site-packages"
    packages.mkdir(parents=True)
    pod = tmp_path / "pod"
    pod.mkdir()
    (pod / "sync_site_packages.sh").write_text("#!/bin/sh\n")
    try:
        (packages / ".pod").symlink_to(pod, target_is_directory=True)
    except OSError:
        pytest.skip("Creating symlinks is unavailable")

    assert command._site_packages_missing()

    write_package(packages)
    assert not command._site_packages_missing()


@pytest.mark.parametrize(
    ("platform", "architectures"),
    [
        ("Android", ("arm64-v8a", "x86_64")),
        (
            "iOS",
            ("iphoneos.arm64", "iphonesimulator.arm64", "iphonesimulator.x86_64"),
        ),
    ],
)
def test_every_default_mobile_architecture_needs_packages(
    command, platform, architectures
):
    command.package_platform = platform
    packages = command.build_dir / "site-packages"
    # Unrelated root files and empty ABI directories are not a usable cache.
    write_package(packages)
    for arch in architectures:
        (packages / arch).mkdir()
    assert command._site_packages_missing()

    for arch in architectures[:-1]:
        write_package(packages / arch)
    assert command._site_packages_missing()

    write_package(packages / architectures[-1])
    assert not command._site_packages_missing()

    (packages / architectures[-1] / "flet" / "__init__.pyc").unlink()
    assert command._site_packages_missing()


@pytest.mark.parametrize(
    ("platform", "architecture"),
    [("Android", "arm64-v8a"), ("iOS", "iphoneos.arm64")],
)
def test_only_selected_architectures_need_packages(command, platform, architecture):
    command.package_platform = platform
    command.template_data["options"]["target_arch"] = [architecture]
    write_package(command.build_dir / "site-packages" / architecture)

    assert not command._site_packages_missing()
