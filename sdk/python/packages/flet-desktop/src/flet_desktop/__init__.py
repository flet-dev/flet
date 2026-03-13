import asyncio
import ctypes
import ctypes.util
import logging
import os
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import urllib.request
import zipfile
from pathlib import Path

import flet_desktop
import flet_desktop.version
from flet.utils import (
    get_arch,
    is_linux,
    is_macos,
    is_windows,
    random_string,
    safe_tar_extractall,
)

logger = logging.getLogger(flet_desktop.__name__)

# Supported Linux build targets ordered by glibc version.
# Each entry maps a minimum glibc (major, minor) to a distro_id used in
# release artifact filenames.
_GLIBC_DISTRO_TABLE = [
    ((2, 28), "debian10"),
    ((2, 31), "ubuntu20.04"),
    ((2, 35), "ubuntu22.04"),
    ((2, 36), "debian12"),
    ((2, 39), "ubuntu24.04"),
]


def get_package_bin_dir():
    """
    Return the directory that contains bundled desktop runtime artifacts.

    The directory may contain platform-specific executables or compressed
    archives used to provision the desktop client at runtime.  When the
    package is installed without bundled binaries the directory will be
    empty and the download path is used instead.
    """

    return str(Path(__file__).parent.joinpath("app"))


def __get_desktop_flavor():
    """
    Return the desktop client flavor to use: ``"full"`` or ``"light"``.

    Resolution order:

    1. ``FLET_DESKTOP_FLAVOR`` environment variable.
    2. ``[tool.flet].desktop_flavor`` in the project's ``pyproject.toml``.
    3. Default: ``"light"`` on Linux, ``"full"`` elsewhere.
    """

    env_flavor = os.environ.get("FLET_DESKTOP_FLAVOR", "").strip().lower()
    if env_flavor in ("full", "light"):
        return env_flavor

    # Try reading from pyproject.toml in the current working directory.
    try:
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib  # type: ignore[no-redef]

        pyproject_path = Path(os.getcwd()) / "pyproject.toml"
        if pyproject_path.is_file():
            with pyproject_path.open("rb") as f:
                data = tomllib.load(f)
            flavor = data.get("tool", {}).get("flet", {}).get("desktop_flavor", "")
            if isinstance(flavor, str) and flavor.strip().lower() in (
                "full",
                "light",
            ):
                return flavor.strip().lower()
    except Exception:
        pass

    return "light" if is_linux() else "full"


def __get_system_glibc_version():
    """
    Return the system glibc version as a ``(major, minor)`` tuple.

    Falls back to ``(0, 0)`` when detection fails.
    """

    try:
        libc_name = ctypes.util.find_library("c")
        if not libc_name:
            return (0, 0)
        libc = ctypes.CDLL(libc_name)
        gnu_get_libc_version = libc.gnu_get_libc_version
        gnu_get_libc_version.restype = ctypes.c_char_p
        ver_str = gnu_get_libc_version().decode("ascii")
        parts = ver_str.split(".")
        return (int(parts[0]), int(parts[1]))
    except Exception:
        return (0, 0)


def __get_linux_distro_id():
    """
    Return the distro id to use for downloading the Linux binary archive.

    Uses glibc version detection to pick the best matching build target
    (highest glibc requirement that is <= system glibc).  Can be
    overridden via the ``FLET_LINUX_DISTRO`` environment variable.
    """

    override = os.environ.get("FLET_LINUX_DISTRO", "").strip()
    if override:
        return override

    sys_glibc = __get_system_glibc_version()
    best = None
    for required_glibc, distro_id in _GLIBC_DISTRO_TABLE:
        if sys_glibc >= required_glibc:
            best = distro_id
    if best is None:
        best = _GLIBC_DISTRO_TABLE[0][1]  # oldest as last resort
    return best


def __get_artifact_filename():
    """
    Return the release artifact filename for the current platform.

    Windows: ``flet-windows.zip``
    macOS:   ``flet-macos.tar.gz``
    Linux:   ``flet-linux-{distro}[-light]-{arch}.tar.gz``
    """

    if is_windows():
        return "flet-windows.zip"
    if is_macos():
        return "flet-macos.tar.gz"
    # Linux
    distro = __get_linux_distro_id()
    arch = get_arch()
    flavor = __get_desktop_flavor()
    if flavor == "light":
        return f"flet-linux-{distro}-light-{arch}.tar.gz"
    return f"flet-linux-{distro}-{arch}.tar.gz"


def __get_client_storage_dir():
    """
    Return a versioned local directory used to store unpacked desktop client files.

    The path format is:
    ``~/.flet/client/flet-desktop-{flavor}-{version}``.
    """

    flavor = __get_desktop_flavor()
    return Path.home().joinpath(
        ".flet", "client", f"flet-desktop-{flavor}-{flet_desktop.version.version}"
    )


def __download_flet_client(file_name):
    """
    Download a Flet client archive from GitHub Releases.

    The download URL is constructed from the version embedded in
    ``flet_desktop.version.version``.  It can be overridden entirely
    via the ``FLET_CLIENT_URL`` environment variable.

    Args:
        file_name: Archive filename to download (e.g. ``flet-macos.tar.gz``).

    Returns:
        Local path to the downloaded archive.
    """

    ver = flet_desktop.version.version
    flet_url = f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
    flet_url = os.environ.get("FLET_CLIENT_URL", flet_url)
    logger.info(f"Downloading Flet v{ver} from {flet_url}")
    print(f"Preparing Flet v{ver} for the first use. This is a one-time operation...")
    # Download to a temp name first, then rename for atomicity.
    temp_arch = Path(tempfile.gettempdir()).joinpath(f"{file_name}.{random_string(8)}")
    urllib.request.urlretrieve(flet_url, str(temp_arch))
    final_path = Path(tempfile.gettempdir()).joinpath(file_name)
    temp_arch.rename(final_path)
    return str(final_path)


def ensure_client_cached():
    """
    Ensure the desktop client is extracted in the local cache directory.

    If the cache directory does not exist, looks for a bundled archive in
    the package (for PyInstaller bundles) and falls back to downloading
    from GitHub Releases.

    Returns:
        :class:`Path` to the cache directory containing the unpacked client.
    """

    cache_dir = __get_client_storage_dir()
    if cache_dir.exists():
        logger.info(f"Flet client found in cache: {cache_dir}")
        return cache_dir

    artifact = __get_artifact_filename()

    # Check for a bundled archive (PyInstaller or legacy wheel).
    bundled = os.path.join(get_package_bin_dir(), artifact)
    if os.path.exists(bundled):
        archive_path = bundled
    else:
        archive_path = __download_flet_client(artifact)

    logger.info(f"Extracting Flet client from {archive_path} to {cache_dir}")
    cache_dir.mkdir(parents=True, exist_ok=True)

    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(str(cache_dir))
    else:
        with tarfile.open(archive_path, "r:gz") as tar_arch:
            safe_tar_extractall(tar_arch, str(cache_dir))

    return cache_dir


def open_flet_view(page_url, assets_dir, hidden):
    """
    Start a desktop view process and return the process object and PID file path.

    Args:
        page_url: Page endpoint the desktop client should open.
        assets_dir: Optional assets directory passed to the client process.
        hidden: Whether the window should start hidden.

    Returns:
        A tuple containing:
            - `subprocess.Popen`: started desktop process.
            - `str`: path to a temporary PID file used by [`close_flet_view()`][(m).].
    """

    args, flet_env, pid_file = __locate_and_unpack_flet_view(
        page_url, assets_dir, hidden
    )
    return subprocess.Popen(args, env=flet_env), pid_file


async def open_flet_view_async(page_url, assets_dir, hidden):
    """
    Asynchronously start a desktop view process.

    Args:
        page_url: Page endpoint the desktop client should open.
        assets_dir: Optional assets directory passed to the client process.
        hidden: Whether the window should start hidden.

    Returns:
        A tuple containing:
            - `asyncio.subprocess.Process`: started desktop process.
            - `str`: path to a temporary PID file used by [`close_flet_view()`][(m).].
    """

    args, flet_env, pid_file = __locate_and_unpack_flet_view(
        page_url, assets_dir, hidden
    )
    return (
        await asyncio.create_subprocess_exec(args[0], *args[1:], env=flet_env),
        pid_file,
    )


def close_flet_view(pid_file):
    """
    Terminate a running desktop view process using its PID file.

    The function attempts to read the process ID from `pid_file`, send a
    termination signal, and remove the PID file. Failures while terminating are
    intentionally ignored, but the PID file is removed when possible.

    Args:
        pid_file: Path to the PID file returned by [`open_flet_view()`][(m).]
            or [`open_flet_view_async()`][(m).].
    """

    if pid_file is not None and os.path.exists(pid_file):
        try:
            with open(pid_file, encoding="utf-8") as f:
                fvp_pid = int(f.read())
            logger.debug(f"Flet View process {fvp_pid}")
            os.kill(fvp_pid, signal.SIGKILL)
        except Exception:
            pass
        finally:
            os.remove(pid_file)


def __locate_and_unpack_flet_view(page_url, assets_dir, hidden):
    """
    Resolve desktop client executable, prepare launch arguments, and environment.

    Resolution strategy (per platform):

    1. Prefer app binaries produced by ``flet build`` in the current workspace.
    2. Use ``FLET_VIEW_PATH`` when provided.
    3. Use cached / downloaded client from ``~/.flet/client/``.

    Platform-specific launch commands are prepared for Windows, macOS, and Linux.

    Args:
        page_url: Page endpoint the desktop client should open.
        assets_dir: Optional assets directory passed to the client process.
        hidden: Whether to set ``FLET_HIDE_WINDOW_ON_START=true`` in process env.

    Returns:
        A tuple containing:
            - ``list[str]``: command arguments for the desktop client.
            - ``dict[str, str]``: environment variables for the launched process.
            - ``str``: path to the temporary PID file.

    Raises:
        FileNotFoundError: If a required desktop executable or archive
            cannot be located or downloaded.
    """

    logger.info("Starting Flet View app...")

    args = []

    # pid file - Flet client writes its process ID to this file
    pid_file = str(Path(tempfile.gettempdir()).joinpath(random_string(20)))

    if is_windows():
        flet_path = None
        # 1. Try loading Flet client built with the latest run of `flet build`
        build_windows = os.path.join(os.getcwd(), "build", "windows")
        if os.path.exists(build_windows):
            for f in os.listdir(build_windows):
                if f.endswith(".exe"):
                    flet_path = os.path.join(build_windows, f)

        # 2. Check FLET_VIEW_PATH (developer mode)
        if not flet_path:
            flet_view_path = os.environ.get("FLET_VIEW_PATH")
            if flet_view_path and os.path.exists(flet_view_path):
                logger.info(f"Flet View found via FLET_VIEW_PATH: {flet_view_path}")
                flet_path = os.path.join(flet_view_path, "flet.exe")

        # 3. Use cached or downloaded client
        if not flet_path:
            cache_dir = ensure_client_cached()
            flet_path = str(cache_dir.joinpath("flet", "flet.exe"))

        args = [flet_path, page_url, pid_file]

    elif is_macos():
        app_path = None
        # 1. Try loading Flet client built with the latest run of `flet build`
        build_macos = os.path.join(os.getcwd(), "build", "macos")
        if os.path.exists(build_macos):
            for f in os.listdir(build_macos):
                if f.endswith(".app"):
                    app_path = os.path.join(build_macos, f)

        # 2. Check FLET_VIEW_PATH (developer mode)
        if not app_path:
            flet_view_path = os.environ.get("FLET_VIEW_PATH")
            if flet_view_path:
                logger.info(f"Flet.app is set via FLET_VIEW_PATH: {flet_view_path}")
                temp_flet_dir = Path(flet_view_path)
            else:
                # 3. Use cached or downloaded client
                temp_flet_dir = ensure_client_cached()

            app_name = None
            for f in os.listdir(temp_flet_dir):
                if f.endswith(".app"):
                    app_name = f
            if app_name is None:
                raise FileNotFoundError(
                    f"Application bundle not found in {temp_flet_dir}"
                )
            app_path = temp_flet_dir.joinpath(app_name)

        logger.info(f"page_url: {page_url}")
        logger.info(f"pid_file: {pid_file}")
        args = ["open", str(app_path), "-n", "-W", "--args", page_url, pid_file]

    elif is_linux():
        app_path = None
        # 1. Try loading Flet client built with the latest run of `flet build`
        build_linux = os.path.join(os.getcwd(), "build", "linux")
        if os.path.exists(build_linux):
            for f in os.listdir(build_linux):
                ef = os.path.join(build_linux, f)
                if os.path.isfile(ef) and stat.S_IXUSR & os.stat(ef)[stat.ST_MODE]:
                    app_path = ef

        # 2. Check FLET_VIEW_PATH (developer mode)
        if not app_path:
            flet_view_path = os.environ.get("FLET_VIEW_PATH")
            if flet_view_path:
                logger.info(f"Flet View is set via FLET_VIEW_PATH: {flet_view_path}")
                app_path = str(Path(flet_view_path).joinpath("flet"))
            else:
                # 3. Use cached or downloaded client
                cache_dir = ensure_client_cached()
                app_path = str(cache_dir.joinpath("flet", "flet"))

        args = [str(app_path), page_url, pid_file]

    flet_env = {**os.environ}

    if assets_dir:
        args.append(assets_dir)

    if hidden:
        flet_env["FLET_HIDE_WINDOW_ON_START"] = "true"

    return args, flet_env, pid_file
