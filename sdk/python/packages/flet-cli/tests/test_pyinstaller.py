"""Tests for `flet_cli.__pyinstaller`: the PyInstaller hooks and their helpers."""

import os
import shutil
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
    monkeypatch.setattr(
        pyi_utils, "get_artifact_filename", lambda flavor=None: artifact
    )


def _archive(tmp_path: Path) -> Path:
    """Run `archive_flet_bin()` into a fresh directory and return it."""
    out = tmp_path / "out"
    files = pyi_utils.archive_flet_bin(str(out))
    assert files == [str(out / name) for name in _bundled_names(out)]
    return out


def _bundled_names(out: Path) -> list[str]:
    """Names of the files in `out` that get bundled: all but the `.source` stamp."""
    archives = [n for n in os.listdir(out) if not n.startswith(".")]
    archives.sort(key=lambda n: n.endswith(".sha256"))
    return archives


class TestClientArchiveLayout:
    """`archive_flet_bin()` lays out the client the way the runtime unpacks it."""

    def test_windows_client_is_zipped_under_flet(self, tmp_path, monkeypatch):
        """The cached `flet/` client is zipped under `flet/`, without its marker."""
        _use_client(monkeypatch, _make_client(tmp_path / "cache", "windows"), "windows")

        out = _archive(tmp_path)

        assert _bundled_names(out) == [
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

        out = _archive(tmp_path)

        with tarfile.open(out / _ARTIFACTS["linux"]) as tar:
            assert sorted(tar.getnames()) == ["flet", "flet/flet"]

    def test_macos_app_bundle_is_archived_at_root(self, tmp_path, monkeypatch):
        """On macOS the `.app` bundle is archived at the root, keeping its symlinks."""
        cache = _make_client(tmp_path / "cache", "macos")
        (cache / "Flet.app" / "Contents" / "Current").symlink_to("MacOS")
        _use_client(monkeypatch, cache, "macos")

        out = _archive(tmp_path)

        with tarfile.open(out / "flet-macos.tar.gz") as tar:
            names = tar.getnames()
            assert "Flet.app/Contents/MacOS/Flet" in names
            assert ".last-used" not in names
            assert tar.getmember("Flet.app/Contents/Current").issym()


class TestClientArchiveMissingClient:
    """`archive_flet_bin()` builds no archive from a missing or incomplete client."""

    def test_returns_none_without_client(self, tmp_path, monkeypatch):
        """No client to bundle means no archive directory."""
        monkeypatch.setattr(pyi_utils, "get_flet_bin_path", lambda: None)

        assert pyi_utils.archive_flet_bin(str(tmp_path)) is None

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
            pyi_utils.archive_flet_bin(str(tmp_path / "out"))

    def test_incomplete_cached_client_fails(self, tmp_path, monkeypatch):
        """A cached client without its executable fails with a hint to delete it."""
        cache = tmp_path / "cache"
        (cache / "flet").mkdir(parents=True)
        monkeypatch.delenv("FLET_VIEW_PATH", raising=False)
        _use_client(monkeypatch, cache, "windows")

        with pytest.raises(
            RuntimeError, match="cached Flet client .* Delete that directory"
        ):
            pyi_utils.archive_flet_bin(str(tmp_path / "out"))


class TestClientArchiveAtRuntime:
    """The app unpacks the bundled client archive at runtime."""

    def test_bundled_archive_is_used_without_download(self, tmp_path, monkeypatch):
        """`ensure_client_cached()` unpacks the archive without downloading."""
        platform = _host_platform()
        artifact = flet_desktop.get_artifact_filename()
        _use_client(
            monkeypatch, _make_client(tmp_path / "cache", platform), platform, artifact
        )
        bundled = str(_archive(tmp_path))

        def no_download(_):
            raise AssertionError("the client was downloaded")

        monkeypatch.setattr(flet_desktop, "get_package_bin_dir", lambda: bundled)
        monkeypatch.setattr(flet_desktop, "__download_flet_client", no_download)
        monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")

        cache_dir = flet_desktop.ensure_client_cached()

        assert cache_dir.joinpath(*_CLIENT_EXES[platform]).read_bytes() == b"client"


class TestLinuxClientArchiveName:
    """The Linux archive is named after the client it holds."""

    @pytest.mark.parametrize(
        "libs, flavor",
        [
            (["libapp.so", "libmedia_kit_libs_linux_plugin.so"], "full"),
            (["libapp.so", "liburl_launcher_linux_plugin.so"], "light"),
        ],
    )
    def test_flavor_is_read_from_the_client(self, tmp_path, monkeypatch, libs, flavor):
        """A `FLET_VIEW_PATH` client is named by its flavor, not the configured one."""
        view = tmp_path / "view"
        (view / "lib").mkdir(parents=True)
        (view / "flet").write_bytes(b"client")
        for lib in libs:
            (view / "lib" / lib).touch()
        _use_client(monkeypatch, view, "linux")
        flavors = []

        def artifact(flavor=None):
            flavors.append(flavor)
            return f"flet-linux-debian12-{flavor}-amd64.tar.gz"

        monkeypatch.setattr(pyi_utils, "get_artifact_filename", artifact)

        out = _archive(tmp_path)

        assert flavors == [flavor]
        assert _bundled_names(out)[0] == f"flet-linux-debian12-{flavor}-amd64.tar.gz"

    def test_unknown_linux_system_bundles_no_client(
        self, tmp_path, monkeypatch, caplog
    ):
        """No client archive for this system is a warning, not a failed build."""
        _use_client(monkeypatch, _make_client(tmp_path / "cache", "linux"), "linux")

        def artifact(flavor=None):
            raise RuntimeError(
                "Flet desktop client is not available for Linux riscv64."
            )

        monkeypatch.setattr(pyi_utils, "get_artifact_filename", artifact)

        with caplog.at_level("WARNING", logger=pyi_utils.__name__):
            assert pyi_utils.archive_flet_bin(str(tmp_path / "out")) is None
        assert "not available for Linux riscv64" in caplog.text


class TestStagedClientArchive:
    """The staged archive stays valid for PyInstaller's cached analysis."""

    def _stage(self, client: Path, out: Path, name: str = "flet-windows.zip"):
        return pyi_utils.stage_client_archive(str(client), "flet", name, str(out))

    def _client(self, tmp_path: Path) -> Path:
        client = tmp_path / "client"
        client.mkdir()
        (client / "flet.exe").write_bytes(b"client")
        return client

    def test_unchanged_client_is_not_archived_again(self, tmp_path, monkeypatch):
        """The archive of an unchanged client is reused without rebuilding it."""
        client = self._client(tmp_path)
        files = self._stage(client, tmp_path / "out")

        def no_archive(*args):
            raise AssertionError("the archive was rebuilt")

        monkeypatch.setattr(pyi_utils, "write_client_archive", no_archive)

        assert self._stage(client, tmp_path / "out") == files

    @pytest.mark.parametrize(
        "name", ["flet-windows.zip", "flet-linux-debian12-light-amd64.tar.gz"]
    )
    def test_same_content_keeps_the_archive(self, tmp_path, name):
        """A rebuilt archive with the same content keeps its modification time."""
        client = self._client(tmp_path)
        archive, _ = self._stage(client, tmp_path / "out", name)
        os.utime(archive, ns=(0, 0))
        os.utime(client / "flet.exe")

        self._stage(client, tmp_path / "out", name)

        assert os.stat(archive).st_mtime_ns == 0

    def test_changed_content_replaces_the_archive(self, tmp_path):
        """New content replaces the archive, so PyInstaller analyzes again."""
        client = self._client(tmp_path)
        archive, sidecar = self._stage(client, tmp_path / "out")
        os.utime(archive, ns=(0, 0))
        old_fingerprint = Path(sidecar).read_text()
        (client / "flet.exe").write_bytes(b"patched client")

        self._stage(client, tmp_path / "out")

        assert os.stat(archive).st_mtime_ns > 0
        assert Path(sidecar).read_text() != old_fingerprint

    def test_archive_of_another_name_is_removed(self, tmp_path):
        """Only the current archive is left to bundle."""
        client = self._client(tmp_path)
        out = tmp_path / "out"
        self._stage(client, out, "flet-linux-debian12-light-amd64.tar.gz")

        self._stage(client, out, "flet-linux-debian12-amd64.tar.gz")

        assert _bundled_names(out) == [
            "flet-linux-debian12-amd64.tar.gz",
            "flet-linux-debian12-amd64.tar.gz.sha256",
        ]


class TestCopiedClient:
    """`copy_flet_bin()` copies only the client, in the layout `flet pack` expects."""

    def test_flet_view_path_client_is_copied_under_flet(self, tmp_path, monkeypatch):
        """A `FLET_VIEW_PATH` holding `flet.exe` itself is copied as `flet/`."""
        view = tmp_path / "view"
        view.mkdir()
        (view / "flet.exe").write_bytes(b"client")
        _use_client(monkeypatch, view, "windows")

        temp = Path(pyi_utils.copy_flet_bin())
        try:
            assert os.listdir(temp) == ["flet"]
            assert (temp / "flet" / "flet.exe").read_bytes() == b"client"
        finally:
            shutil.rmtree(temp)

    def test_cached_client_is_copied_without_markers(self, tmp_path, monkeypatch):
        """The cache markers next to the client are left behind."""
        _use_client(monkeypatch, _make_client(tmp_path / "cache", "windows"), "windows")

        temp = Path(pyi_utils.copy_flet_bin())
        try:
            assert os.listdir(temp) == ["flet"]
        finally:
            shutil.rmtree(temp)
