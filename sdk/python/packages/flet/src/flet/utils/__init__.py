import os
import socket
import sys
from pathlib import Path

from flet_core.utils import Vector, is_mobile, slugify


def get_package_root_dir():
    return str(Path(__file__).parent.parent)


if not is_mobile():
    import webbrowser


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


def is_localhost_url(url):
    return (
        "://localhost/" in url
        or "://localhost:" in url
        or "://127.0.0.1/" in url
        or "://127.0.0.1:" in url
    )


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
