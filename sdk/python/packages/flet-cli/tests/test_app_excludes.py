import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

from flet_cli.utils import app_excludes
from flet_cli.utils.app_excludes import find_default_excludes


def _touch(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch()


def _venv(path: Path):
    _touch(path / "pyvenv.cfg")
    _touch(path / "lib" / "site-packages" / "pkg" / "__init__.py")
    _touch(path / "lib" / "site-packages" / "pkg" / "__pycache__" / "x.pyc")


@pytest.fixture
def app(tmp_path: Path) -> Path:
    _touch(tmp_path / "main.py")
    _touch(tmp_path / "assets" / "icon.png")
    return tmp_path


def test_plain_app_has_no_default_excludes(app: Path):
    assert find_default_excludes(app) == []


def test_top_level_hidden_entries_excluded(app: Path):
    for name in [".git", ".flet", ".idea"]:
        (app / name).mkdir()
    _touch(app / ".env")
    _touch(app / ".DS_Store")

    assert find_default_excludes(app) == [
        ".DS_Store",
        ".env",
        ".flet",
        ".git",
        ".idea",
    ]


def test_nested_hidden_entries_kept(app: Path):
    _touch(app / "pkg" / ".data" / "file.txt")
    _touch(app / "pkg" / ".hidden")

    assert find_default_excludes(app) == []


def test_venv_detected_by_pyvenv_cfg(app: Path):
    _venv(app / "venv")
    _venv(app / "src" / ".venv")
    _touch(app / "env" / "__init__.py")

    assert find_default_excludes(app) == sorted(["venv", os.path.join("src", ".venv")])


def test_pycache_excluded_at_any_depth(app: Path):
    _touch(app / "__pycache__" / "main.cpython-312.pyc")
    _touch(app / "src" / "__pycache__" / "a.pyc")
    _touch(app / "pkg" / "sub" / "__pycache__" / "b.pyc")

    assert find_default_excludes(app) == sorted(
        [
            "__pycache__",
            os.path.join("pkg", "sub", "__pycache__"),
            os.path.join("src", "__pycache__"),
        ]
    )


def test_excluded_dirs_are_not_walked(app: Path):
    _venv(app / "venv")

    assert find_default_excludes(app) == ["venv"]


def test_include_keeps_entries(app: Path):
    (app / ".git").mkdir()
    _touch(app / ".env")
    _touch(app / "src" / "__pycache__" / "a.pyc")

    assert find_default_excludes(app, [".env", "src/__pycache__"]) == [".git"]


def test_included_hidden_dir_is_still_scanned(app: Path):
    _touch(app / ".config" / "__pycache__" / "a.pyc")

    assert find_default_excludes(app, [".config"]) == [
        os.path.join(".config", "__pycache__")
    ]


def test_hidden_attribute_honored(app: Path, monkeypatch: pytest.MonkeyPatch):
    _touch(app / "desktop.ini")
    _touch(app / "pkg" / "desktop.ini")

    real_is_hidden = app_excludes._is_hidden
    monkeypatch.setattr(
        app_excludes,
        "_is_hidden",
        lambda entry: entry.name == "desktop.ini" or real_is_hidden(entry),
    )

    assert find_default_excludes(app) == ["desktop.ini"]


@pytest.mark.skipif(sys.platform != "win32", reason="Windows file attributes")
def test_windows_hidden_attribute(app: Path):
    _touch(app / "secret.txt")
    _touch(app / "pkg" / "secret.txt")
    for p in [app / "secret.txt", app / "pkg" / "secret.txt"]:
        subprocess.run(["attrib", "+h", str(p)], check=True)
    assert os.stat(app / "secret.txt").st_file_attributes & (stat.FILE_ATTRIBUTE_HIDDEN)

    assert find_default_excludes(app) == ["secret.txt"]


def test_already_excluded_paths_are_not_scanned(app: Path):
    _touch(app / "build" / "python" / "__pycache__" / "a.pyc")
    _touch(app / ".tox" / "x")
    _touch(app / "src" / "vendor" / "__pycache__" / "b.pyc")

    assert find_default_excludes(app, exclude=["build", ".tox", "src/vendor"]) == []
