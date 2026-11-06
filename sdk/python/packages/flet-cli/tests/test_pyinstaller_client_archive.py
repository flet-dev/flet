import os
import tarfile
import zipfile
from pathlib import Path

import flet_cli.__pyinstaller.utils as pyi_utils
import flet_desktop
from flet.utils import is_macos


def _make_client(root: Path, macos: bool) -> Path:
    """Lay out a cached desktop client the way `ensure_client_cached()` leaves it."""
    root.mkdir(parents=True)
    (root / ".last-used").touch()
    if macos:
        exe = root / "Flet.app" / "Contents" / "MacOS" / "Flet"
    else:
        exe = root / "flet" / "flet.exe"
    exe.parent.mkdir(parents=True)
    exe.write_bytes(b"client")
    return root


def _use_client(monkeypatch, bin_path: Path, macos: bool, artifact: str) -> None:
    """Make `archive_flet_bin()` see `bin_path` as the client of the given platform."""
    monkeypatch.setattr(pyi_utils, "get_flet_bin_path", lambda: str(bin_path))
    monkeypatch.setattr(pyi_utils, "is_macos", lambda: macos)
    monkeypatch.setattr(pyi_utils, "get_artifact_filename", lambda: artifact)


def test_archives_windows_client_as_zip(tmp_path, monkeypatch):
    """The cached `flet/` client is zipped under `flet/`, without the cache marker."""
    _use_client(
        monkeypatch, _make_client(tmp_path / "cache", False), False, "flet-windows.zip"
    )

    out = Path(pyi_utils.archive_flet_bin())

    assert sorted(os.listdir(out)) == ["flet-windows.zip", "flet-windows.zip.sha256"]
    with zipfile.ZipFile(out / "flet-windows.zip") as zf:
        assert zf.namelist() == ["flet/flet.exe"]


def test_archives_flet_view_path_client_under_flet(tmp_path, monkeypatch):
    """A `FLET_VIEW_PATH` directory holding the client itself is archived as `flet/`."""
    view = tmp_path / "view"
    view.mkdir()
    (view / "flet").write_bytes(b"client")
    _use_client(monkeypatch, view, False, "flet-linux-ubuntu24.04-amd64.tar.gz")

    out = Path(pyi_utils.archive_flet_bin())

    with tarfile.open(out / "flet-linux-ubuntu24.04-amd64.tar.gz") as tar:
        assert sorted(tar.getnames()) == ["flet", "flet/flet"]


def test_archives_macos_app_bundle(tmp_path, monkeypatch):
    """On macOS the `.app` bundle is archived at the root, keeping its symlinks."""
    cache = _make_client(tmp_path / "cache", True)
    (cache / "Flet.app" / "Contents" / "Current").symlink_to("MacOS")
    _use_client(monkeypatch, cache, True, "flet-macos.tar.gz")

    out = Path(pyi_utils.archive_flet_bin())

    with tarfile.open(out / "flet-macos.tar.gz") as tar:
        names = tar.getnames()
        assert "Flet.app/Contents/MacOS/Flet" in names
        assert ".last-used" not in names
        assert tar.getmember("Flet.app/Contents/Current").issym()


def test_returns_none_without_client(monkeypatch):
    """No client to bundle means no archive directory."""
    monkeypatch.setattr(pyi_utils, "get_flet_bin_path", lambda: None)

    assert pyi_utils.archive_flet_bin() is None


def test_bundled_archive_is_used_without_download(tmp_path, monkeypatch):
    """`ensure_client_cached()` unpacks the archive and never downloads the client."""
    macos = is_macos()
    artifact = flet_desktop.get_artifact_filename()
    _use_client(monkeypatch, _make_client(tmp_path / "cache", macos), macos, artifact)
    bundled = pyi_utils.archive_flet_bin()

    def no_download(_):
        raise AssertionError("the client was downloaded")

    monkeypatch.setattr(flet_desktop, "get_package_bin_dir", lambda: bundled)
    monkeypatch.setattr(flet_desktop, "__download_flet_client", no_download)
    monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")

    cache_dir = flet_desktop.ensure_client_cached()

    exe = ("Flet.app", "Contents", "MacOS", "Flet") if macos else ("flet", "flet.exe")
    assert cache_dir.joinpath(*exe).read_bytes() == b"client"
