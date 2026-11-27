"""Choosing the Linux desktop client to download.

The client is built against several glibc versions. A system whose glibc is
older than the oldest build has no client to run.
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


class TestLinuxClientArtifact:
    @pytest.mark.parametrize(
        "arch, glibc, filename",
        [
            ("amd64", (2, 31), "flet-linux-ubuntu20.04-amd64.tar.gz"),
            ("arm64", (2, 31), "flet-linux-ubuntu20.04-arm64.tar.gz"),
            ("amd64", (2, 34), "flet-linux-ubuntu20.04-amd64.tar.gz"),
            ("arm64", (2, 36), "flet-linux-debian12-arm64.tar.gz"),
            ("arm64", (2, 41), "flet-linux-ubuntu24.04-arm64.tar.gz"),
        ],
    )
    def test_picks_newest_build_the_system_can_run(self, linux, arch, glibc, filename):
        """The newest build whose glibc the system meets is chosen."""
        linux(arch, glibc)
        assert flet_desktop.get_artifact_filename() == filename

    @pytest.mark.parametrize("arch", ["amd64", "arm64"])
    def test_glibc_older_than_any_build_fails(self, linux, arch):
        """A glibc older than the oldest build raises, naming the required one."""
        linux(arch, (2, 28))
        with pytest.raises(RuntimeError, match=rf"Linux {arch} requires glibc 2\.31"):
            flet_desktop.get_artifact_filename()

    @pytest.mark.parametrize("arch", ["amd64", "arm64"])
    def test_undetected_glibc_falls_back_to_oldest_build(self, linux, arch, caplog):
        """An undetectable glibc falls back to the oldest build, with a warning."""
        linux(arch, (0, 0))
        assert (
            flet_desktop.get_artifact_filename()
            == f"flet-linux-ubuntu20.04-{arch}.tar.gz"
        )
        assert "Could not detect glibc version" in caplog.text

    def test_architecture_without_builds_fails(self, linux):
        """An architecture with no builds raises."""
        linux("arm_7", (2, 36))
        with pytest.raises(RuntimeError, match="not available for Linux arm_7"):
            flet_desktop.get_artifact_filename()

    def test_flet_linux_distro_overrides_detection(self, linux, monkeypatch):
        """`FLET_LINUX_DISTRO` is used as is, whatever the system glibc."""
        linux("arm64", (2, 28))
        monkeypatch.setenv("FLET_LINUX_DISTRO", "ubuntu22.04")
        assert (
            flet_desktop.get_artifact_filename()
            == "flet-linux-ubuntu22.04-arm64.tar.gz"
        )

    def test_unknown_flet_linux_distro_fails(self, linux, monkeypatch):
        """A `FLET_LINUX_DISTRO` that names no build raises, listing the builds."""
        linux("amd64", (2, 39))
        monkeypatch.setenv("FLET_LINUX_DISTRO", "debian10")
        with pytest.raises(
            RuntimeError, match="FLET_LINUX_DISTRO=debian10.*ubuntu20.04"
        ):
            flet_desktop.get_artifact_filename()
