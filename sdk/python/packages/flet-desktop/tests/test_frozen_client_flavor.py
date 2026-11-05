"""Frozen apps keep the flavor of the Linux client bundled by flet pack."""

import sys
import tarfile
from pathlib import Path

import pytest

import flet_desktop


@pytest.fixture
def frozen_linux(tmp_path, monkeypatch):
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
        pytest.fail(f"Downloaded {artifact} instead of using the bundled client")

    monkeypatch.setattr(flet_desktop, "__download_flet_client", download)
    return tmp_path


@pytest.mark.parametrize("flavor", ["full", "light"])
def test_extracts_bundled_flavor_despite_nearby_project(frozen_linux, flavor):
    other_flavor = "light" if flavor == "full" else "full"
    (frozen_linux / "pyproject.toml").write_text(
        f'[tool.flet]\ndesktop_flavor = "{other_flavor}"\n'
    )
    suffix = "-light" if flavor == "light" else ""
    artifact = f"flet-linux-debian12{suffix}-amd64.tar.gz"
    executable = frozen_linux / "patched-client"
    executable.write_bytes(b"client with custom icon and metadata")
    with tarfile.open(frozen_linux / artifact, "w:gz") as archive:
        archive.add(executable, arcname="flet/flet")

    assert flet_desktop.get_artifact_filename() == artifact
    cache = flet_desktop.ensure_client_cached()
    assert cache.name.startswith(f"flet-desktop-{flavor}-debian12-")
    assert (cache / "flet" / "flet").read_bytes() == executable.read_bytes()
    assert flet_desktop.ensure_client_cached() == cache


@pytest.mark.parametrize("flavor", ["full", "light"])
def test_explicit_environment_overrides_bundled_flavor(
    frozen_linux, monkeypatch, flavor
):
    other_suffix = "-light" if flavor == "full" else ""
    (frozen_linux / f"flet-linux-debian12{other_suffix}-amd64.tar.gz").touch()
    monkeypatch.setenv("FLET_DESKTOP_FLAVOR", flavor)

    suffix = "-light" if flavor == "light" else ""
    assert flet_desktop.get_artifact_filename() == (
        f"flet-linux-debian12{suffix}-amd64.tar.gz"
    )


def test_frozen_app_without_archive_ignores_nearby_project(frozen_linux):
    (frozen_linux / "pyproject.toml").write_text(
        '[tool.flet]\ndesktop_flavor = "full"\n'
    )
    assert flet_desktop.get_artifact_filename() == (
        "flet-linux-debian12-light-amd64.tar.gz"
    )
