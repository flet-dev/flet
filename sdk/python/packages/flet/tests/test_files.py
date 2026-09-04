import os
import stat
import tempfile

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
