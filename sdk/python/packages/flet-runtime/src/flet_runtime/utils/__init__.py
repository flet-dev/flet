import hashlib
import os
import shutil
import socket
import sys
from pathlib import Path

from flet_core.types import WebRenderer
from flet_runtime.utils.once import Once
from flet_runtime.utils.patch_index import patch_index_html, patch_manifest_json


def get_bool_env_var(name: str):
    v = os.getenv(name)
    return v.lower() in ["true", "1", "yes"] if v is not None else None


def is_ios():
    return os.getenv("FLET_PLATFORM") == "ios"


def is_android():
    return os.getenv("FLET_PLATFORM") == "android"


def is_embedded():
    return os.getenv("FLET_PLATFORM") is not None


def is_mobile():
    return is_ios() or is_android()


if not is_mobile():
    import platform
    import webbrowser


def is_windows():
    return not is_mobile() and platform.system() == "Windows"


def is_linux():
    return not is_mobile() and platform.system() == "Linux"


def is_linux_server():
    if not is_mobile() and platform.system() == "Linux":
        # check if it's WSL
        p = "/proc/version"
        if os.path.exists(p):
            with open(p, "r") as file:
                if "microsoft" in file.read():
                    return False  # it's WSL, not a server
        return os.environ.get("DISPLAY") is None
    return False


def is_macos():
    return not is_mobile() and platform.system() == "Darwin"


def get_platform():
    p = platform.system() if not is_mobile() else ""
    if is_windows():
        return "windows"
    elif p == "Linux":
        return "linux"
    elif p == "Darwin":
        return "darwin"
    else:
        raise Exception(f"Unsupported platform: {p}")


def get_arch():
    a = platform.machine().lower() if not is_mobile() else ""
    if a == "x86_64" or a == "amd64":
        return "amd64"
    elif a == "arm64" or a == "aarch64":
        return "arm64"
    elif a.startswith("arm"):
        return "arm_7"
    else:
        raise Exception(f"Unsupported architecture: {a}")


def open_in_browser(url):
    if not is_mobile():
        webbrowser.open(url)


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


def is_within_directory(directory, target):
    abs_directory = os.path.abspath(directory)
    abs_target = os.path.abspath(target)

    prefix = os.path.commonprefix([abs_directory, abs_target])

    return prefix == abs_directory


def safe_tar_extractall(tar, path=".", members=None, *, numeric_owner=False):
    for member in tar.getmembers():
        member_path = os.path.join(path, member.name)
        if not is_within_directory(path, member_path):
            raise Exception("Attempted Path Traversal in Tar File")

    tar.extractall(path, members, numeric_owner=numeric_owner)


def is_localhost_url(url):
    return (
        "://localhost/" in url
        or "://localhost:" in url
        or "://127.0.0.1/" in url
        or "://127.0.0.1:" in url
    )


try:
    from flet.utils import get_package_root_dir
except ImportError:

    def get_package_root_dir():
        return str(Path(__file__).parent)


def get_package_bin_dir():
    return os.path.join(get_package_root_dir(), "bin")


def get_package_web_dir():
    web_root_dir = os.environ.get("FLET_WEB_PATH")
    return web_root_dir if web_root_dir else os.path.join(get_package_root_dir(), "web")


def get_free_tcp_port():
    sock = socket.socket()
    sock.bind(("", 0))
    return sock.getsockname()[1]


def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        return local_ip
    except Exception:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)


def get_current_script_dir():
    pathname = os.path.dirname(sys.argv[0])
    return os.path.abspath(pathname)


def calculate_file_hash(path, blocksize=65536):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            data = f.read(blocksize)
            if not data:
                break
            h.update(data)
    return h.hexdigest()


def copy_tree(src, dst, ignore=None):
    return shutil.copytree(src, dst, ignore=ignore, symlinks=True, dirs_exist_ok=True)


def sha1(input_string):
    sha1_hash = hashlib.sha1()
    sha1_hash.update(input_string.encode("utf-8"))
    return sha1_hash.hexdigest()
