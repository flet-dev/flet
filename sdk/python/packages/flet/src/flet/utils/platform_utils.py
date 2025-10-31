import asyncio
import os
import sys

from flet.controls.exceptions import FletUnsupportedPlatformException


def get_bool_env_var(name: str):
    v = os.getenv(name)
    return v.lower() in ["true", "1", "yes"] if v is not None else None


def is_asyncio():
    try:
        return asyncio.current_task() is not None or sys.platform == "emscripten"
    except RuntimeError:
        return False


def is_pyodide():
    return sys.platform == "emscripten"


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


def is_windows():
    return not is_mobile() and platform.system() == "Windows"


def is_linux():
    return not is_mobile() and platform.system() == "Linux"


def is_linux_server():
    if not is_mobile() and platform.system() == "Linux":
        # check if it's WSL
        p = "/proc/version"
        if os.path.exists(p):
            with open(p, encoding="utf-8") as file:
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
        raise FletUnsupportedPlatformException(f"Unsupported platform: {p}")


def get_arch():
    a = platform.machine().lower() if not is_mobile() else ""
    if a == "x86_64" or a == "amd64":
        return "amd64"
    elif a == "arm64" or a == "aarch64":
        return "arm64"
    elif a.startswith("arm"):
        return "arm_7"
    else:
        raise FletUnsupportedPlatformException(f"Unsupported architecture: {a}")
