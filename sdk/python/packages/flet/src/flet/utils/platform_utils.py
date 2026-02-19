import asyncio
import os
import sys

from flet.controls.exceptions import FletUnsupportedPlatformException


def get_bool_env_var(name: str):
    """
    Parses an environment variable value as a boolean.

    Args:
        name: Environment variable name.

    Returns:
        `True` when the variable value is `true`, `1`, or `yes` (case-insensitive);
        `False` for any other defined value; `None` when the variable is not set.
    """
    v = os.getenv(name)
    return v.lower() in ["true", "1", "yes"] if v is not None else None


def is_asyncio():
    """
    Indicates whether execution is inside an active asyncio task.

    This function also returns `True` on Pyodide, where the default execution model
    is asynchronous even when no current task is available.

    Returns:
        `True` when an asyncio task is active or when running on Pyodide, otherwise
        `False`.
    """
    try:
        return asyncio.current_task() is not None or sys.platform == "emscripten"
    except RuntimeError:
        return False


def is_pyodide():
    """
    Indicates whether Python is running in a Pyodide environment.

    Returns:
        `True` when `sys.platform` is `emscripten`, otherwise `False`.
    """
    return sys.platform == "emscripten"


def is_ios():
    """
    Indicates whether the target platform is iOS.

    Returns:
        `True` when `FLET_PLATFORM=ios`, otherwise `False`.
    """
    return os.getenv("FLET_PLATFORM") == "ios"


def is_android():
    """
    Indicates whether the target platform is Android.

    Returns:
        `True` when `FLET_PLATFORM=android`, otherwise `False`.
    """
    return os.getenv("FLET_PLATFORM") == "android"


def is_embedded():
    """
    Indicates whether a platform is explicitly provided by the embedding runtime.

    Returns:
        `True` when `FLET_PLATFORM` is set, otherwise `False`.
    """
    return os.getenv("FLET_PLATFORM") is not None


def is_mobile():
    """
    Indicates whether the target platform is mobile.

    Returns:
        `True` when targeting iOS or Android, otherwise `False`.
    """
    return is_ios() or is_android()


if not is_mobile():
    import platform


def is_windows():
    """
    Indicates whether the current non-mobile host platform is Windows.

    Returns:
        `True` on Windows hosts when not targeting mobile, otherwise `False`.
    """
    return not is_mobile() and platform.system() == "Windows"


def is_linux():
    """
    Indicates whether the current non-mobile host platform is Linux.

    Returns:
        `True` on Linux hosts when not targeting mobile, otherwise `False`.
    """
    return not is_mobile() and platform.system() == "Linux"


def is_linux_server():
    """
    Indicates whether the current environment is a headless Linux server.

    The environment is considered a Linux server when:
    - the host platform is Linux and not mobile;
    - it is not Windows Subsystem for Linux (WSL);
    - the `DISPLAY` environment variable is not set.

    Returns:
        `True` for headless Linux server environments, otherwise `False`.
    """
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
    """
    Indicates whether the current non-mobile host platform is macOS.

    Returns:
        `True` on macOS hosts when not targeting mobile, otherwise `False`.
    """
    return not is_mobile() and platform.system() == "Darwin"


def get_platform():
    """
    Returns the normalized platform identifier used by Flet.

    Returns:
        One of: `windows`, `linux`, or `darwin`.

    Raises:
        [`FletUnsupportedPlatformException`][flet.]: If the current platform is
            unsupported.
    """
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
    """
    Returns the normalized CPU architecture identifier used by Flet.

    Returns:
        One of: `amd64`, `arm64`, or `arm_7`.

    Raises:
        [`FletUnsupportedPlatformException`][flet.]: If the current architecture is
            unsupported.
    """
    a = platform.machine().lower() if not is_mobile() else ""
    if a == "x86_64" or a == "amd64":
        return "amd64"
    elif a == "arm64" or a == "aarch64":
        return "arm64"
    elif a.startswith("arm"):
        return "arm_7"
    else:
        raise FletUnsupportedPlatformException(f"Unsupported architecture: {a}")
