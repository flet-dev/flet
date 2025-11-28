import os
import shutil
import sys


def is_within_directory(directory, target):
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    prefix = os.path.commonprefix([abs_directory, abs_target])

    return prefix == abs_directory


def safe_tar_extractall(tar, path=".", members=None, *, numeric_owner=False):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not is_within_directory(path, member_path):
            raise RuntimeError("Attempted Path Traversal in Tar File")

    tar.extractall(path, members, numeric_owner=numeric_owner)


def copy_tree(src, dst, ignore=None):
    return shutil.copytree(src, dst, ignore=ignore, symlinks=True, dirs_exist_ok=True)


# https://stackoverflow.com/questions/377017/test-if-executable-exists-in-python
def which(program, exclude_exe=None):
    import os

    def is_exe(fpath):
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
    pathname = os.path.dirname(sys.argv[0])
    return os.path.abspath(pathname)
