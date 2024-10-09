import os
import socket
import sys

from flet_core.utils import Vector, is_mobile, slugify


def open_in_browser(url):
    if not is_mobile():
        import webbrowser

        webbrowser.open(url)


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
