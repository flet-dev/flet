import os
import shutil
import sys


def is_within_directory(directory, target):
    """
    Checks whether `target` is located within `directory`.

    Args:
        directory: Base directory path.
        target: Candidate path to validate.

    Returns:
        `True` if `target` resolves under `directory`, otherwise `False`.
    """
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    prefix = os.path.commonprefix([abs_directory, abs_target])

    return prefix == abs_directory


def safe_tar_extractall(tar, path=".", members=None, *, numeric_owner=False):
    """
    Extracts a tar archive after validating member paths.

    The function prevents path traversal by ensuring each archive member resolves
    within the destination directory.

    Args:
        tar: Open `tarfile.TarFile` object.
        path: Destination directory.
        members: Optional member subset to extract.
        numeric_owner: Whether to use numeric user/group IDs.

    Raises:
        RuntimeError: If a member attempts to escape the destination directory.
    """
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not is_within_directory(path, member_path):
            raise RuntimeError("Attempted Path Traversal in Tar File")

    tar.extractall(path, members, numeric_owner=numeric_owner)


def copy_tree(src, dst, ignore=None):
    """
    Copies a directory tree into `dst`.

    This wrapper preserves symlinks and allows copying into an existing
    destination directory.

    Args:
        src: Source directory path.
        dst: Destination directory path.
        ignore: Optional callable used to ignore names during copy.

    Returns:
        The destination directory path.
    """
    return shutil.copytree(src, dst, ignore=ignore, symlinks=True, dirs_exist_ok=True)


# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program, exclude_exe=None):
    """
    Finds the first executable matching `program` in `PATH`.

    Args:
        program: Executable filename to search for.
        exclude_exe: Absolute executable path to skip when searching.

    Returns:
        Absolute path to the first matching executable, or `None` if not found.
    """
    import os

    def is_exe(fpath):
        """
        Checks whether `fpath` points to an executable file.

        Args:
            fpath: Candidate file path.

        Returns:
            `True` if `fpath` exists and is executable, otherwise `False`.
        """
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    for path in os.environ["PATH"].split(os.pathsep):
        exe_file = os.path.join(path, program)
        if is_exe(exe_file) and (
            exclude_exe is None
            or (exclude_exe is not None and exclude_exe.lower() != exe_file.lower())
        ):
            return exe_file

    return None


def cleanup_path(path: str, executable: str):
    """
    Removes directories containing a given executable from a PATH-like string.

    The check also removes directories containing Windows launcher variants:
    `<executable>.bat` and `<executable>.cmd`.

    Args:
        path: PATH-like string separated by `os.pathsep`.
        executable: Executable name to filter out.

    Returns:
        Filtered PATH-like string.
    """
    cleaned_dirs = []
    for path_dir in path.split(os.pathsep):
        found = False
        for file_name in [executable, f"{executable}.bat", f"{executable}.cmd"]:
            if os.path.isfile(os.path.join(path_dir, file_name)):
                found = True
                break
        if not found:
            cleaned_dirs.append(path_dir)

    return os.pathsep.join(cleaned_dirs)


def get_current_script_dir():
    """
    Returns the absolute directory of the current script entry point.

    Returns:
        Absolute directory path derived from `sys.argv[0]`.
    """
    pathname = os.path.dirname(sys.argv[0])
    return os.path.abspath(pathname)
