"""Which Linux client a frozen app, made with `flet pack` or PyInstaller, uses.

A frozen app bundles the client archive built for the build machine's distro
and flavor. At runtime it uses that archive, or downloads the client this
system can run.
"""

import logging
import sys
import tarfile
from pathlib import Path

import pytest

import flet_desktop


class _Downloaded(Exception):
    """Raised by the fake download, carrying the requested artifact."""


@pytest.fixture
def frozen_linux(tmp_path, monkeypatch):
    """A frozen amd64 Linux app on a glibc 2.36 (Debian 12) system.

    Returns the app's bundle directory, which is also the working directory.
    """
    monkeypatch.delenv("FLET_DESKTOP_FLAVOR", raising=False)
    monkeypatch.delenv("FLET_LINUX_DISTRO", raising=False)
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(flet_desktop, "is_linux", lambda: True)
    monkeypatch.setattr(flet_desktop, "is_windows", lambda: False)
    monkeypatch.setattr(flet_desktop, "is_macos", lambda: False)
    monkeypatch.setattr(flet_desktop, "get_arch", lambda: "amd64")
    monkeypatch.setattr(flet_desktop, "__get_system_glibc_version", lambda: (2, 36))
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")
    monkeypatch.setattr(flet_desktop, "get_package_bin_dir", lambda: str(tmp_path))
    monkeypatch.chdir(tmp_path)

    def download(artifact):
        raise _Downloaded(artifact)

    monkeypatch.setattr(flet_desktop, "__download_flet_client", download)
    return tmp_path


def _bundle(bundle: Path, artifact: str, content: bytes = b"bundled client") -> None:
    """Writes a client archive named `artifact` into the app's bundle."""
    executable = bundle / "client"
    executable.write_bytes(content)
    with tarfile.open(bundle / artifact, "w:gz") as archive:
        archive.add(executable, arcname="flet/flet")
    executable.unlink()


class TestBundledFlavor:
    """The flavor of the bundled client wins over a nearby `pyproject.toml`."""

    @pytest.mark.parametrize("flavor", ["full", "light"])
    def test_extracts_bundled_flavor_despite_nearby_project(self, frozen_linux, flavor):
        """The bundled client is extracted even when a project asks for the other."""
        other_flavor = "light" if flavor == "full" else "full"
        (frozen_linux / "pyproject.toml").write_text(
            f'[tool.flet]\ndesktop_flavor = "{other_flavor}"\n'
        )
        suffix = "-light" if flavor == "light" else ""
        artifact = f"flet-linux-debian12{suffix}-amd64.tar.gz"
        content = b"client with custom icon and metadata"
        _bundle(frozen_linux, artifact, content)

        assert flet_desktop.get_artifact_filename() == artifact
        cache = flet_desktop.ensure_client_cached()
        assert cache.name.startswith(f"flet-desktop-{flavor}-debian12-")
        assert (cache / "flet" / "flet").read_bytes() == content
        assert flet_desktop.ensure_client_cached() == cache

    @pytest.mark.parametrize("flavor", ["full", "light"])
    def test_explicit_environment_overrides_bundled_flavor(
        self, frozen_linux, monkeypatch, flavor
    ):
        """`FLET_DESKTOP_FLAVOR` picks the flavor over the bundled client's."""
        other_suffix = "-light" if flavor == "full" else ""
        (frozen_linux / f"flet-linux-debian12{other_suffix}-amd64.tar.gz").touch()
        monkeypatch.setenv("FLET_DESKTOP_FLAVOR", flavor)

        suffix = "-light" if flavor == "light" else ""
        assert flet_desktop.get_artifact_filename() == (
            f"flet-linux-debian12{suffix}-amd64.tar.gz"
        )

    def test_frozen_app_without_archive_ignores_nearby_project(self, frozen_linux):
        """Without a bundled client, the Linux default flavor is used."""
        (frozen_linux / "pyproject.toml").write_text(
            '[tool.flet]\ndesktop_flavor = "full"\n'
        )
        assert flet_desktop.get_artifact_filename() == (
            "flet-linux-debian12-light-amd64.tar.gz"
        )


class TestBundledClientFromAnotherDistro:
    """Which client a frozen app uses when its bundle is for another distro."""

    def test_light_client_from_older_distro_is_used(self, frozen_linux):
        """A light client built on an older glibc runs here without a download."""
        _bundle(frozen_linux, "flet-linux-ubuntu20.04-light-amd64.tar.gz")

        assert flet_desktop.get_artifact_filename() == (
            "flet-linux-ubuntu20.04-light-amd64.tar.gz"
        )
        cache = flet_desktop.ensure_client_cached()
        assert cache.name.startswith("flet-desktop-light-ubuntu20.04-")
        assert (cache / "flet" / "flet").read_bytes() == b"bundled client"

    def test_newest_usable_light_client_is_used(self, frozen_linux):
        """Of several bundled light clients, the newest one this glibc runs wins."""
        for distro in ("ubuntu20.04", "ubuntu22.04", "ubuntu24.04"):
            _bundle(frozen_linux, f"flet-linux-{distro}-light-amd64.tar.gz")

        assert flet_desktop.get_artifact_filename() == (
            "flet-linux-ubuntu22.04-light-amd64.tar.gz"
        )

    def test_light_client_from_newer_distro_is_downloaded(self, frozen_linux):
        """A light client built on a newer glibc is replaced by a download."""
        _bundle(frozen_linux, "flet-linux-ubuntu24.04-light-amd64.tar.gz")

        with pytest.raises(_Downloaded, match="flet-linux-debian12-light-amd64"):
            flet_desktop.ensure_client_cached()

    def test_full_client_from_another_distro_keeps_full_flavor(
        self, frozen_linux, caplog
    ):
        """A full client for another distro downloads this distro's full client."""
        _bundle(frozen_linux, "flet-linux-ubuntu20.04-amd64.tar.gz")

        with (
            caplog.at_level(logging.WARNING, logger=flet_desktop.__name__),
            pytest.raises(_Downloaded, match="flet-linux-debian12-amd64.tar.gz"),
        ):
            flet_desktop.ensure_client_cached()
        assert "built for ubuntu20.04" in caplog.text

    def test_flavor_from_environment_skips_bundled_light_client(
        self, frozen_linux, monkeypatch
    ):
        """`FLET_DESKTOP_FLAVOR=full` doesn't reuse a bundled light client."""
        _bundle(frozen_linux, "flet-linux-ubuntu20.04-light-amd64.tar.gz")
        monkeypatch.setenv("FLET_DESKTOP_FLAVOR", "full")

        assert flet_desktop.get_artifact_filename() == (
            "flet-linux-debian12-amd64.tar.gz"
        )

    def test_unfrozen_app_ignores_bundle_dir(self, frozen_linux, monkeypatch):
        """Outside a frozen app the client is picked from the system glibc only."""
        _bundle(frozen_linux, "flet-linux-ubuntu20.04-light-amd64.tar.gz")
        monkeypatch.setattr(sys, "frozen", False)

        assert flet_desktop.get_artifact_filename() == (
            "flet-linux-debian12-light-amd64.tar.gz"
        )
