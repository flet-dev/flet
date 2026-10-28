import sys
from pathlib import Path

import pytest

from flet_cli.__pyinstaller.extensions import (
    find_imported_modules,
    find_installed_extensions,
    find_missing_extensions,
    get_client_extensions,
)


def _install(site_packages: Path, name: str, files: list[str]) -> None:
    """Install a fake distribution whose RECORD lists `files`."""
    for relative in files:
        path = site_packages / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("")
    dist_info = site_packages / f"{name.replace('-', '_')}-1.0.0.dist-info"
    dist_info.mkdir(parents=True)
    (dist_info / "METADATA").write_text(
        f"Metadata-Version: 2.1\nName: {name}\nVersion: 1.0.0\n"
    )
    record = [*files, f"{dist_info.name}/METADATA", f"{dist_info.name}/RECORD"]
    (dist_info / "RECORD").write_text("".join(f"{r},,\n" for r in record))


@pytest.fixture
def site_packages(tmp_path, monkeypatch) -> Path:
    """An empty site-packages directory that is the whole of `sys.path`."""
    path = tmp_path / "site-packages"
    path.mkdir()
    monkeypatch.setattr(sys, "path", [str(path)])
    return path


def test_client_extensions_read_from_snapshot(tmp_path):
    """Package URIs in the snapshot name the client's packages."""
    snapshot = tmp_path / "app.so"
    snapshot.write_bytes(
        b"\0package:flet/src/a.dart\0package:flet_audio/x.dart"
        b"\0package:flet_map/y.dart\0package:Bad/z\0"
    )
    assert get_client_extensions(str(snapshot)) == {"flet", "flet_audio", "flet_map"}


def test_client_extensions_unknown_without_flet_library(tmp_path):
    """A snapshot that names no `flet` library, or no snapshot, tells nothing."""
    snapshot = tmp_path / "app.so"
    snapshot.write_bytes(b"package:flet_audio/x.dart")
    assert get_client_extensions(str(snapshot)) is None
    assert get_client_extensions(str(tmp_path / "missing.so")) is None


def test_installed_extensions_from_record(site_packages):
    """Distributions installing a Flutter package are extensions with their modules."""
    _install(
        site_packages,
        "my-ext",
        [
            "my_ext/__init__.py",
            "my_ext_helpers.py",
            "flutter/my_ext/pubspec.yaml",
            "flutter/my_ext/lib/my_ext.dart",
        ],
    )
    _install(site_packages, "plain", ["plain/__init__.py"])

    [extension] = find_installed_extensions()
    assert extension.package == "my_ext"
    assert extension.distribution == "my-ext"
    assert extension.modules == {"my_ext", "my_ext_helpers"}


def test_installed_extensions_from_editable_install(site_packages, tmp_path):
    """An unowned `flutter/<name>` folder next to a `<name>` module is an extension."""
    src = tmp_path / "src"
    for name in ("dev_ext", "3.47.7"):
        (src / "flutter" / name).mkdir(parents=True)
        (src / "flutter" / name / "pubspec.yaml").write_text("")
    (src / "dev_ext").mkdir()
    sys.path.append(str(src))

    [extension] = find_installed_extensions()
    assert extension.package == "dev_ext"
    assert extension.distribution is None
    assert extension.modules == {"dev_ext"}


def test_imported_modules_skip_environments_and_output(tmp_path):
    """Imports are collected from app files, not venvs, hidden or build folders."""
    (tmp_path / "main.py").write_text("import flet as ft\nfrom pkg.mod import x\n")
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "mod.py").write_text("from . import y\nimport a.b, c\n")
    (tmp_path / "broken.py").write_text("import (\n")
    for skipped in (".hidden", "build", "venv"):
        (tmp_path / skipped).mkdir()
        (tmp_path / skipped / "x.py").write_text(f"import from_{skipped[-4:]}\n")
    (tmp_path / "venv" / "pyvenv.cfg").write_text("")

    assert find_imported_modules(tmp_path) == {"flet", "pkg", "a", "c"}


def test_imported_modules_skip_symlinked_folders_and_unreadable_files(tmp_path):
    """A folder linking to its parent and a dangling file link don't stop the scan."""
    (tmp_path / "main.py").write_text("import flet\n")
    (tmp_path / "loop").symlink_to(tmp_path, target_is_directory=True)
    (tmp_path / "legacy.py").symlink_to(tmp_path / "missing.py")

    assert find_imported_modules(tmp_path) == {"flet"}


def test_missing_extensions_are_imported_and_not_in_client(site_packages, tmp_path):
    """Only imported extensions the client lacks are reported."""
    for name in ("in_client", "unused", "missing"):
        _install(
            site_packages,
            name,
            [f"{name}/__init__.py", f"flutter/{name}/pubspec.yaml"],
        )
    app = tmp_path / "app"
    app.mkdir()
    (app / "main.py").write_text("import in_client\nimport missing\n")

    missing = find_missing_extensions(app, {"flet", "in_client"})
    assert [e.package for e in missing] == ["missing"]
