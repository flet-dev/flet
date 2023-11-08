import json
import os
import re
import shutil
import socket
import sys
from pathlib import Path
from typing import Optional

from flet_core.types import WebRenderer


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
        return os.environ.get("XDG_CURRENT_DESKTOP") is None
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
    except Exception as e:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)


def get_current_script_dir():
    pathname = os.path.dirname(sys.argv[0])
    return os.path.abspath(pathname)


def patch_index_html(
    index_path: str,
    base_href: str,
    websocket_endpoint_path: Optional[str] = None,
    app_name: Optional[str] = None,
    app_description: Optional[str] = None,
    pyodide: bool = False,
    pyodide_pre: bool = False,
    pyodide_script_path: str = "",
    web_renderer: WebRenderer = WebRenderer.AUTO,
    use_color_emoji: bool = False,
    route_url_strategy: str = "path",
):
    with open(index_path, "r") as f:
        index = f.read()

    if pyodide and pyodide_script_path:
        module_name = Path(pyodide_script_path).stem
        pyodideCode = f"""
        <script>
            var micropipIncludePre = {str(pyodide_pre).lower()};
            var pythonModuleName = "{module_name}";
        </script>
        <script src="python.js"></script>
        """
        index = index.replace("<!-- pyodideCode -->", pyodideCode)
    index = index.replace("%FLET_WEB_PYODIDE%", str(pyodide).lower())
    index = index.replace(
        "<!-- webRenderer -->",
        f'<script>webRenderer="{web_renderer.value}";</script>',
    )
    index = index.replace(
        "<!-- useColorEmoji -->",
        f"<script>useColorEmoji={str(use_color_emoji).lower()};</script>",
    )
    index = index.replace("%FLET_ROUTE_URL_STRATEGY%", route_url_strategy)

    if base_href:
        base_url = base_href.strip("/").strip()
        index = index.replace(
            '<base href="/">',
            '<base href="{}">'.format(
                "/" if base_url == "" else "/{}/".format(base_url)
            ),
        )
    if websocket_endpoint_path:
        index = re.sub(
            r"\<meta name=\"flet-websocket-endpoint-path\" content=\"(.+)\">",
            r'<meta name="flet-websocket-endpoint-path" content="{}">'.format(
                websocket_endpoint_path
            ),
            index,
        )
    if app_name:
        index = re.sub(
            r"\<meta name=\"apple-mobile-web-app-title\" content=\"(.+)\">",
            r'<meta name="apple-mobile-web-app-title" content="{}">'.format(app_name),
            index,
        )
    if app_description:
        index = re.sub(
            r"\<meta name=\"description\" content=\"(.+)\">",
            r'<meta name="description" content="{}">'.format(app_description),
            index,
        )

    with open(index_path, "w") as f:
        f.write(index)


def patch_manifest_json(
    manifest_path: str,
    app_name: Optional[str] = None,
    app_short_name: Optional[str] = None,
    app_description: Optional[str] = None,
):
    with open(manifest_path, "r") as f:
        manifest = json.loads(f.read())

    if app_name:
        manifest["name"] = app_name
        manifest["short_name"] = app_name

    if app_short_name:
        manifest["short_name"] = app_short_name

    if app_description:
        manifest["description"] = app_description

    with open(manifest_path, "w") as f:
        f.write(json.dumps(manifest, indent=2))


def copy_tree(src, dst):
    """Recursively copy a directory tree using shutil.copy2().

    Arguments:
    src -- source directory path
    dst -- destination directory path

    Return a list of files that were copied or might have been copied.
    """
    if not os.path.isdir(src):
        raise OSError("Source is not a directory")

    os.makedirs(dst, exist_ok=True)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_tree(s, d)
        else:
            shutil.copy2(s, d)
