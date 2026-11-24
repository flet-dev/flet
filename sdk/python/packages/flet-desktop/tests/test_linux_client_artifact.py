"""Choosing the Linux desktop client to download.

The client is built against several glibc versions, but not every one of
them for every architecture: there is no Debian 10 (glibc 2.28) build for
arm64, so an arm64 system with an older glibc has no client to run.
"""

import pytest

import flet_desktop


@pytest.fixture
def linux(monkeypatch):
    monkeypatch.delenv("FLET_LINUX_DISTRO", raising=False)
    monkeypatch.setattr(flet_desktop, "is_windows", lambda: False)
    monkeypatch.setattr(flet_desktop, "is_macos", lambda: False)
    monkeypatch.setattr(flet_desktop, "__get_desktop_flavor", lambda: "full")

    def configure(arch, glibc):
        monkeypatch.setattr(flet_desktop, "get_arch", lambda: arch)
        monkeypatch.setattr(flet_desktop, "__get_system_glibc_version", lambda: glibc)

    return configure


@pytest.mark.parametrize(
    "arch, glibc, filename",
    [
        ("amd64", (2, 28), "flet-linux-debian10-amd64.tar.gz"),
        ("amd64", (2, 31), "flet-linux-ubuntu20.04-amd64.tar.gz"),
        ("arm64", (2, 31), "flet-linux-ubuntu20.04-arm64.tar.gz"),
        ("arm64", (2, 36), "flet-linux-debian12-arm64.tar.gz"),
        ("arm64", (2, 41), "flet-linux-ubuntu24.04-arm64.tar.gz"),
    ],
)
def test_picks_newest_build_the_system_can_run(linux, arch, glibc, filename):
    linux(arch, glibc)
    assert flet_desktop.get_artifact_filename() == filename


def test_arm64_with_glibc_older_than_any_arm64_build_fails(linux):
    linux("arm64", (2, 28))
    with pytest.raises(RuntimeError, match=r"Linux arm64 requires glibc 2\.31"):
        flet_desktop.get_artifact_filename()


def test_undetected_glibc_falls_back_to_oldest_build_for_arch(linux):
    linux("arm64", (0, 0))
    assert flet_desktop.get_artifact_filename() == "flet-linux-ubuntu20.04-arm64.tar.gz"


def test_architecture_without_builds_fails(linux):
    linux("arm_7", (2, 36))
    with pytest.raises(RuntimeError, match="not available for Linux arm_7"):
        flet_desktop.get_artifact_filename()


def test_flet_linux_distro_overrides_detection(linux, monkeypatch):
    linux("arm64", (2, 28))
    monkeypatch.setenv("FLET_LINUX_DISTRO", "debian10")
    assert flet_desktop.get_artifact_filename() == "flet-linux-debian10-arm64.tar.gz"
