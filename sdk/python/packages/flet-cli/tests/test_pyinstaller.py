"""Tests for `flet_cli.__pyinstaller`: the PyInstaller hooks and their helpers."""

import os
import tarfile
import zipfile
from pathlib import Path

import pytest

import flet_cli.__pyinstaller.utils as pyi_utils
import flet_desktop
from flet.utils import is_macos, is_windows

_ARTIFACTS = {
    "windows": "flet-windows.zip",
    "linux": "flet-linux-ubuntu24.04-amd64.tar.gz",
    "macos": "flet-macos.tar.gz",
}
_CLIENT_EXES = {
    "windows": ("flet", "flet.exe"),
    "linux": ("flet", "flet"),
    "macos": ("Flet.app", "Contents", "MacOS", "Flet"),
}


def _host_platform() -> str:
    """Name of the platform the tests run on, as used by the helpers below."""
    if is_windows():
        return "windows"
    return "macos" if is_macos() else "linux"


def _make_client(root: Path, platform: str) -> Path:
    """Lay out a cached desktop client the way `ensure_client_cached()` leaves it."""
    root.mkdir(parents=True)
    (root / ".last-used").touch()
    exe = root.joinpath(*_CLIENT_EXES[platform])
    exe.parent.mkdir(parents=True)
    exe.write_bytes(b"client")
    return root


def _use_client(
    monkeypatch, bin_path: Path, platform: str, artifact: str | None = None
) -> None:
    """Make `archive_flet_bin()` see `bin_path` as the client of `platform`."""
    monkeypatch.setattr(pyi_utils, "get_flet_bin_path", lambda: str(bin_path))
    monkeypatch.setattr(pyi_utils, "is_macos", lambda: platform == "macos")
    monkeypatch.setattr(pyi_utils, "is_windows", lambda: platform == "windows")
    artifact = artifact or _ARTIFACTS[platform]
    monkeypatch.setattr(pyi_utils, "get_artifact_filename", lambda: artifact)


class TestClientArchiveLayout:
    """`archive_flet_bin()` lays out the client the way the runtime unpacks it."""

    def test_windows_client_is_zipped_under_flet(self, tmp_path, monkeypatch):
        """The cached `flet/` client is zipped under `flet/`, without its marker."""
        _use_client(monkeypatch, _make_client(tmp_path / "cache", "windows"), "windows")

        out = Path(pyi_utils.archive_flet_bin())

        assert sorted(os.listdir(out)) == [
            "flet-windows.zip",
            "flet-windows.zip.sha256",
        ]
        with zipfile.ZipFile(out / "flet-windows.zip") as zf:
            assert zf.namelist() == ["flet/flet.exe"]

    def test_flet_view_path_client_is_archived_under_flet(self, tmp_path, monkeypatch):
        """A `FLET_VIEW_PATH` directory holding the client itself becomes `flet/`."""
        view = tmp_path / "view"
        view.mkdir()
        (view / "flet").write_bytes(b"client")
        _use_client(monkeypatch, view, "linux")

        out = Path(pyi_utils.archive_flet_bin())

        with tarfile.open(out / _ARTIFACTS["linux"]) as tar:
            assert sorted(tar.getnames()) == ["flet", "flet/flet"]

    def test_macos_app_bundle_is_archived_at_root(self, tmp_path, monkeypatch):
        """On macOS the `.app` bundle is archived at the root, keeping its symlinks."""
        cache = _make_client(tmp_path / "cache", "macos")
        (cache / "Flet.app" / "Contents" / "Current").symlink_to("MacOS")
        _use_client(monkeypatch, cache, "macos")

        out = Path(pyi_utils.archive_flet_bin())

        with tarfile.open(out / "flet-macos.tar.gz") as tar:
            names = tar.getnames()
            assert "Flet.app/Contents/MacOS/Flet" in names
            assert ".last-used" not in names
            assert tar.getmember("Flet.app/Contents/Current").issym()


class TestClientArchiveMissingClient:
    """`archive_flet_bin()` builds no archive from a missing or incomplete client."""

    def test_returns_none_without_client(self, monkeypatch):
        """No client to bundle means no archive directory."""
        monkeypatch.setattr(pyi_utils, "get_flet_bin_path", lambda: None)

        assert pyi_utils.archive_flet_bin() is None

    @pytest.mark.parametrize(
        "platform, exe",
        [("windows", "flet.exe"), ("linux", "flet"), ("macos", ".app bundle")],
    )
    def test_flet_view_path_without_client_fails(
        self, tmp_path, monkeypatch, platform, exe
    ):
        """A `FLET_VIEW_PATH` without the client executable fails the build."""
        view = tmp_path / "view"
        view.mkdir()
        monkeypatch.setenv("FLET_VIEW_PATH", str(view))
        _use_client(monkeypatch, view, platform)

        with pytest.raises(RuntimeError, match=f"FLET_VIEW_PATH .* holds no {exe}"):
            pyi_utils.archive_flet_bin()

    def test_incomplete_cached_client_fails(self, tmp_path, monkeypatch):
        """A cached client without its executable fails with a hint to delete it."""
        cache = tmp_path / "cache"
        (cache / "flet").mkdir(parents=True)
        monkeypatch.delenv("FLET_VIEW_PATH", raising=False)
        _use_client(monkeypatch, cache, "windows")

        with pytest.raises(
            RuntimeError, match="cached Flet client .* Delete that directory"
        ):
            pyi_utils.archive_flet_bin()


class TestClientArchiveAtRuntime:
    """The app unpacks the bundled client archive at runtime."""

    def test_bundled_archive_is_used_without_download(self, tmp_path, monkeypatch):
        """`ensure_client_cached()` unpacks the archive without downloading."""
        platform = _host_platform()
        artifact = flet_desktop.get_artifact_filename()
        _use_client(
            monkeypatch, _make_client(tmp_path / "cache", platform), platform, artifact
        )
        bundled = pyi_utils.archive_flet_bin()

        def no_download(_):
            raise AssertionError("the client was downloaded")

        monkeypatch.setattr(flet_desktop, "get_package_bin_dir", lambda: bundled)
        monkeypatch.setattr(flet_desktop, "__download_flet_client", no_download)
        monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")

        cache_dir = flet_desktop.ensure_client_cached()

        assert cache_dir.joinpath(*_CLIENT_EXES[platform]).read_bytes() == b"client"
