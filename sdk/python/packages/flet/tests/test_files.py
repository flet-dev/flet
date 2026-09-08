import os
import stat
import sys
import tempfile
from unittest.mock import patch

import pytest

from flet.utils import rmtree


def test_rmtree_removes_readonly_files():
    temp_dir = tempfile.mkdtemp()
    sub_dir = os.path.join(temp_dir, "subdir")
    os.makedirs(sub_dir)

    readonly_file = os.path.join(sub_dir, "readonly.idx")
    with open(readonly_file, "w") as fp:
        fp.write("index-data")

    # Set file to read-only (which fails on Windows with standard shutil.rmtree)
    os.chmod(readonly_file, stat.S_IREAD)

    rmtree(temp_dir)
    assert not os.path.exists(temp_dir)


def test_rmtree_nonexistent_directory():
    # Should not raise exception
    nonexistent = os.path.join(tempfile.gettempdir(), "nonexistent_dir_12345")
    rmtree(nonexistent)


@pytest.mark.parametrize("py_version", [(3, 11, 0), (3, 12, 0)])
def test_rmtree_raises_permission_error_when_deletion_fails(py_version):
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "locked.txt")
    with open(test_file, "w") as fp:
        fp.write("locked")

    try:
        with (
            patch("sys.version_info", py_version),
            patch("os.unlink", side_effect=PermissionError("File locked")),
            pytest.raises(PermissionError),
        ):
            rmtree(temp_dir)
    finally:
        if os.path.exists(temp_dir):
            rmtree(temp_dir, ignore_errors=True)


@pytest.mark.parametrize("py_version", [(3, 11, 0), (3, 12, 0)])
def test_rmtree_ignore_errors_when_deletion_fails(py_version):
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "locked.txt")
    with open(test_file, "w") as fp:
        fp.write("locked")

    try:
        with (
            patch("sys.version_info", py_version),
            patch("os.unlink", side_effect=PermissionError("File locked")),
        ):
            rmtree(temp_dir, ignore_errors=True)
    finally:
        if os.path.exists(temp_dir):
            import shutil

            shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-specific file locking")
def test_rmtree_raises_permission_error_on_locked_file_windows():
    temp_dir = tempfile.mkdtemp()
    test_file = os.path.join(temp_dir, "locked.txt")
    with open(test_file, "w") as fp:
        fp.write("locked")

    # On Windows, keeping an open handle locks the file from deletion
    with open(test_file), pytest.raises(PermissionError):
        rmtree(temp_dir)

    if os.path.exists(temp_dir):
        rmtree(temp_dir, ignore_errors=True)
