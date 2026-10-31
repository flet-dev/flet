import asyncio
import contextlib
import ctypes
import ctypes.util
import functools
import hashlib
import logging
import os
import shutil
import signal
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import urllib.request
import zipfile
from pathlib import Path

from rich.progress import Progress

import flet_desktop
import flet_desktop.version
from flet.utils import (
    get_arch,
    is_linux,
    is_macos,
    is_windows,
    random_string,
    safe_tar_extractall,
    safe_zip_extractall,
)
from flet_desktop.extensions import (
    find_extension_packages,
    find_imported_modules,
    find_installed_extensions,
    get_client_extensions,
)

logger = logging.getLogger(flet_desktop.__name__)

# Supported Linux build targets ordered by glibc version.
# Each entry maps a minimum glibc (major, minor) to a distro_id used in
# release artifact filenames, and the architectures it is built for.
_GLIBC_DISTRO_TABLE = [
    ((2, 28), "debian10", ("amd64",)),
    ((2, 31), "ubuntu20.04", ("amd64", "arm64")),
    ((2, 35), "ubuntu22.04", ("amd64", "arm64")),
    ((2, 36), "debian12", ("amd64", "arm64")),
    ((2, 39), "ubuntu24.04", ("amd64", "arm64")),
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


def __read_pyproject_flavor(pyproject_path: Path) -> str | None:
    """
    Return `[tool.flet].desktop_flavor` from a `pyproject.toml`, if valid.

    Args:
        pyproject_path: Path of the `pyproject.toml` to read.

    Returns:
        `"full"` or `"light"`, or `None` when the file is missing, unreadable
            or has no valid setting.
    """

    try:
        if sys.version_info >= (3, 11):
            import tomllib
        else:
            import tomli as tomllib  # type: ignore[no-redef]

        if not pyproject_path.is_file():
            return None
        with pyproject_path.open("rb") as f:
            data = tomllib.load(f)
        flavor = data.get("tool", {}).get("flet", {}).get("desktop_flavor", "")
        if isinstance(flavor, str) and flavor.strip().lower() in ("full", "light"):
            return flavor.strip().lower()
    except Exception:
        pass
    return None


def __get_configured_desktop_flavor() -> str | None:
    """
    Return the desktop client flavor the user configured, or `None`.

    Resolution order:

    1. `FLET_DESKTOP_FLAVOR` environment variable.
    2. `[tool.flet].desktop_flavor` in the `pyproject.toml` of the current
       working directory.
    3. `[tool.flet].desktop_flavor` in the nearest `pyproject.toml` at or
       above the directory of the started script, `sys.argv[0]`, so an app
       started from another directory reads its own project's setting. It is
       skipped when `sys.argv[0]` is not a file, as with `python -c`.

    A frozen app, such as one made with `flet pack`, uses only the environment
    variable: its bundled client must not be swapped for one picked by a
    `pyproject.toml` in the directory it is started from or installed in.

    Invalid values are ignored.
    """

    env_flavor = os.environ.get("FLET_DESKTOP_FLAVOR", "").strip().lower()
    if env_flavor in ("full", "light"):
        return env_flavor
    if getattr(sys, "frozen", False):
        return None

    candidates = [Path(os.getcwd()) / "pyproject.toml"]
    script = Path(sys.argv[0] if sys.argv else "")
    with contextlib.suppress(OSError):
        if script.is_file():
            for directory in script.resolve().parents:
                pyproject_path = directory / "pyproject.toml"
                if pyproject_path.is_file():
                    if pyproject_path != candidates[0]:
                        candidates.append(pyproject_path)
                    break
    for pyproject_path in candidates:
        flavor = __read_pyproject_flavor(pyproject_path)
        if flavor:
            return flavor
    return None


def __get_desktop_flavor():
    """
    Return the desktop client flavor to use: `"full"` or `"light"`.

    The configured flavor (see `__get_configured_desktop_flavor()`) wins;
    otherwise `"light"` on Linux and `"full"` elsewhere.
    """

    return __get_configured_desktop_flavor() or ("light" if is_linux() else "full")


def __get_cached_client_extensions(
    client_dir: Path, snapshot_path: Path
) -> set[str] | None:
    """
    Return the Flutter packages compiled into a cached client.

    They are read from the client's AOT snapshot once and stored in an
    `.extensions` file in its cache directory, so later starts don't scan the
    snapshot again.

    Args:
        client_dir: Cache directory of the client.
        snapshot_path: Path to the client's AOT snapshot.

    Returns:
        Names of the packages, or `None` when they can't be told.
    """

    marker = client_dir / ".extensions"
    with contextlib.suppress(OSError):
        extensions = set(marker.read_text().split())
        if "flet" in extensions:
            return extensions
    extensions = get_client_extensions(str(snapshot_path))
    if extensions is not None:
        with contextlib.suppress(OSError):
            marker.write_text("\n".join(sorted(extensions)))
    return extensions


def __warn_missing_extensions(
    client_dir: Path, snapshot_path: Path, app_dir: str | Path | None
) -> None:
    """
    Warn about the extensions the app uses that the cached client doesn't include.

    Their controls render as unknown controls and their services never
    answer, without either pointing at the client. An extension counts as used
    when its module is already imported or one of the app's Python files
    imports it. On Linux, the light client suggests the full one, which
    includes more extensions; otherwise a client made with `flet build`, which
    Flet uses when the app is started from its project folder, is suggested.
    Problems while checking are logged at debug level and never stop the app.

    Args:
        client_dir: Cache directory of the client.
        snapshot_path: Path to the client's AOT snapshot.
        app_dir: Directory of the app's main script, or `None` to use the
            directory of `sys.argv[0]` when that is a file.
    """

    try:
        client_extensions = __get_cached_client_extensions(client_dir, snapshot_path)
        if client_extensions is None:
            return
        if find_extension_packages() <= client_extensions:
            return
        missing = [
            e for e in find_installed_extensions() if e.package not in client_extensions
        ]
        if not missing:
            return
        imported = {name.split(".")[0] for name in list(sys.modules)}
        if any(not e.modules & imported for e in missing):
            if app_dir is None:
                script = Path(sys.argv[0] if sys.argv else "")
                app_dir = script.resolve().parent if script.is_file() else None
            if app_dir is not None:
                imported |= find_imported_modules(Path(app_dir))
        light = is_linux() and __get_desktop_flavor() == "light"
        for extension in (e for e in missing if e.modules & imported):
            source = (
                f" (from {extension.distribution})" if extension.distribution else ""
            )
            if light:
                fix = (
                    "If the full client includes it, set FLET_DESKTOP_FLAVOR=full "
                    'or desktop_flavor = "full" under [tool.flet] in pyproject.toml: '
                    "https://flet.dev/docs/getting-started/installation#linux"
                )
            else:
                fix = (
                    "Build a client that includes it with `flet build` and start the "
                    "app from the project folder: https://flet.dev/docs/extend/"
                    "user-extensions#change-python-files"
                )
            logger.warning(
                f"The {'light ' if light else ''}Flet desktop client doesn't include "
                f"the {extension.package} extension{source} the app uses, so its "
                f"controls show as unknown controls and its services don't respond. "
                f"{fix}"
            )
    except Exception as e:
        logger.debug(f"Could not check the client's extensions: {e}")


@functools.cache
def __get_system_glibc_version():
    """
    Return the system glibc version as a `(major, minor)` tuple.

    Falls back to `(0, 0)` when detection fails. The result is cached for the
    process, since the system glibc can't change while it runs.
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


def __get_linux_distro_id(arch: str):
    """
    Return the distro id to use for downloading the Linux binary archive.

    Uses glibc version detection to pick the best matching build target
    for `arch` (highest glibc requirement that is <= system glibc).  Can be
    overridden via the `FLET_LINUX_DISTRO` environment variable.

    Raises:
        RuntimeError: If the system glibc is older than every build for `arch`.
    """

    override = os.environ.get("FLET_LINUX_DISTRO", "").strip()
    if override:
        return override
    return __get_glibc_distro_id(arch)


def __get_glibc_distro_id(arch: str):
    """
    Return the distro id of the newest build target the system glibc supports.
    """

    targets = [
        (required_glibc, distro_id)
        for required_glibc, distro_id, arches in _GLIBC_DISTRO_TABLE
        if arch in arches
    ]
    if not targets:
        raise RuntimeError(f"Flet desktop client is not available for Linux {arch}.")
    sys_glibc = __get_system_glibc_version()
    best = None
    for required_glibc, distro_id in targets:
        if sys_glibc >= required_glibc:
            best = distro_id
    if best is None:
        oldest_glibc, oldest = targets[0]
        if sys_glibc == (0, 0):
            logger.warning(
                "Could not detect glibc version, "
                f"falling back to {oldest}. Set FLET_LINUX_DISTRO to override."
            )
            return oldest
        raise RuntimeError(
            f"Flet desktop client for Linux {arch} requires glibc "
            f"{oldest_glibc[0]}.{oldest_glibc[1]} or newer, "
            f"but this system has glibc {sys_glibc[0]}.{sys_glibc[1]}."
        )
    return best


def get_artifact_filename():
    """
    Return the release artifact filename for the current platform.

    Windows: `flet-windows.zip`
    macOS:   `flet-macos.tar.gz`
    Linux:   `flet-linux-{distro}[-light]-{arch}.tar.gz`
    """

    if is_windows():
        return "flet-windows.zip"
    if is_macos():
        return "flet-macos.tar.gz"
    # Linux
    arch = get_arch()
    distro = __get_linux_distro_id(arch)
    flavor = __get_desktop_flavor()
    if flavor == "light":
        return f"flet-linux-{distro}-light-{arch}.tar.gz"
    return f"flet-linux-{distro}-{arch}.tar.gz"


def __get_client_storage_dir(fingerprint: str | None = None) -> Path:
    """
    Return a versioned local directory used to store unpacked desktop client files.

    The path format is: `~/.flet/client/flet-desktop-{flavor}-{version}`, with a
    `-{fingerprint}` suffix when the client comes from a bundled archive.
    Fingerprinting keeps clients patched by `flet pack` (custom icon/metadata)
    from being shadowed by — or shadowing — the vanilla client or another
    app's patched client of the same Flet version.

    On Linux the name is `flet-desktop-{flavor}-{distro}-{version}`. Each distro
    build links the `libmpv` soname of that distro, so a client extracted before
    an OS upgrade or a `FLET_LINUX_DISTRO` change is never reused.

    Args:
        fingerprint: Optional content fingerprint of the bundled client archive.

    Returns:
        Path of the cache directory for this client.
    """

    flavor = __get_desktop_flavor()
    if is_linux():
        name = (
            f"flet-desktop-{flavor}-{__get_linux_distro_id(get_arch())}-"
            f"{flet_desktop.version.version}"
        )
    else:
        name = f"flet-desktop-{flavor}-{flet_desktop.version.version}"
    if fingerprint:
        name += f"-{fingerprint}"
    return Path.home().joinpath(".flet", "client", name)


def __is_hex(value: str) -> bool:
    """
    Return whether `value` is a non-empty lowercase hexadecimal string.

    Args:
        value: String to check.
    """

    return bool(value) and all(c in "0123456789abcdef" for c in value)


def __get_archive_fingerprint(archive_path: str) -> str:
    """
    Return a short content fingerprint for a client archive.

    Prefers a pre-computed `<archive>.sha256` sidecar (written by `flet pack`
    at build time) holding `<hash> <size>`; the recorded size must still match
    the archive, so a replaced archive next to a stale sidecar is re-hashed
    instead of silently mapping to the old client's cache. Falls back to
    hashing the archive, caching the result next to it when possible.

    Args:
        archive_path: Path of the client archive to fingerprint.

    Returns:
        First 12 hex digits of the archive's SHA-256.
    """

    size = os.path.getsize(archive_path)
    fp_file = archive_path + ".sha256"
    try:
        if os.path.exists(fp_file):
            with open(fp_file) as f:
                parts = f.read().split()
            # The hash must be well-formed as well as current: it becomes part
            # of a directory name, and the GC below only recognizes hex ones.
            if len(parts) == 2 and parts[1] == str(size):
                fp = parts[0].lower()
                if len(fp) == 64 and __is_hex(fp):
                    return fp[:12]
    except OSError:
        pass
    h = hashlib.sha256()
    with open(archive_path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    fp = h.hexdigest()
    with contextlib.suppress(OSError), open(fp_file, "w") as f:
        f.write(f"{fp} {size}")
    return fp[:12]


def __gc_stale_client_dirs(cache_dir: Path, max_age_days: int = 30) -> None:
    """
    Best-effort eviction of superseded fingerprinted cache siblings.

    Removes sibling dirs whose name differs from `cache_dir` only in the
    `-{fingerprint}` suffix and that were not used for `max_age_days` (tracked
    via a `.last-used` marker). Dirs are renamed before deletion, so a dir whose
    files are in use by a running app fails the rename on Windows and is left
    untouched. Leftovers of interrupted deletions are swept too.

    Args:
        cache_dir: Cache directory of the client in use; its siblings with the
            same name up to the fingerprint are candidates.
        max_age_days: Days a sibling must have been unused before eviction.
    """

    parent = cache_dir.parent
    prefix = cache_dir.name.rpartition("-")[0] + "-"
    now = time.time()
    try:
        entries = list(parent.iterdir())
    except OSError:
        return
    for entry in entries:
        name = entry.name
        if name.startswith(".trash-"):
            shutil.rmtree(entry, ignore_errors=True)
            continue
        suffix = name[len(prefix) :]
        if (
            not name.startswith(prefix)
            or name == cache_dir.name
            or len(suffix) != 12
            or not __is_hex(suffix)
        ):
            continue
        try:
            marker = entry / ".last-used"
            last_used = max(
                marker.stat().st_mtime if marker.exists() else 0,
                entry.stat().st_mtime,
            )
            if now - last_used < max_age_days * 86400:
                continue
            trash = parent / f".trash-{random_string(8)}"
            entry.rename(trash)
            shutil.rmtree(trash, ignore_errors=True)
        except OSError:
            continue


def __download_with_progress(url, dest_path, description):
    """Download a file to dest_path, showing a rich progress bar."""
    with urllib.request.urlopen(url) as response, Progress(transient=True) as progress:
        content_length = response.headers.get("Content-Length")
        task = progress.add_task(
            description, total=int(content_length) if content_length else None
        )
        with open(dest_path, "wb") as f:
            while chunk := response.read(8192):
                f.write(chunk)
                progress.update(task, advance=len(chunk))


def __download_flet_client(file_name):
    """
    Download a Flet client archive from GitHub Releases.

    The download URL is constructed from the version embedded in
    `flet_desktop.version.version`.  It can be overridden entirely
    via the `FLET_CLIENT_URL` environment variable.

    Args:
        file_name: Archive filename to download (e.g. `flet-macos.tar.gz`).

    Returns:
        Local path to the downloaded archive.
    """

    ver = flet_desktop.version.version
    flet_url = f"https://github.com/flet-dev/flet/releases/download/v{ver}/{file_name}"
    flet_url = os.environ.get("FLET_CLIENT_URL", flet_url)
    logger.info(f"Downloading Flet v{ver} from {flet_url}")
    print(f"Preparing Flet v{ver} for the first use. This is a one-time operation...")
    temp_arch = Path(tempfile.gettempdir()).joinpath(f"{file_name}.{random_string(10)}")
    __download_with_progress(flet_url, str(temp_arch), f"Downloading Flet v{ver}...")
    return str(temp_arch)


def ensure_client_cached():
    """
    Ensure the desktop client is extracted in the local cache directory.

    If the cache directory does not exist, looks for a bundled archive in
    the package (for PyInstaller bundles) and falls back to downloading
    from GitHub Releases.

    Returns:
        :class:`Path` to the cache directory containing the unpacked client.
    """

    artifact = get_artifact_filename()

    # Check for a bundled archive (PyInstaller or legacy wheel). Bundled
    # archives are content-fingerprinted so that a client patched by
    # `flet pack` gets its own cache directory.
    bundled = os.path.join(get_package_bin_dir(), artifact)
    archive_path = bundled if os.path.exists(bundled) else None
    fingerprint = __get_archive_fingerprint(archive_path) if archive_path else None

    cache_dir = __get_client_storage_dir(fingerprint)
    if cache_dir.exists():
        logger.info(f"Flet client found in cache: {cache_dir}")
        with contextlib.suppress(OSError):
            (cache_dir / ".last-used").touch()
        return cache_dir

    if archive_path is None:
        archive_path = __download_flet_client(artifact)

    # Extract to a temp directory first, then atomically rename to the cache
    # directory.  This prevents a partially extracted cache from being treated
    # as valid on a subsequent run.
    temp_extract = cache_dir.parent / f"{cache_dir.name}.{random_string(8)}"
    temp_extract.mkdir(parents=True, exist_ok=True)

    logger.info(f"Extracting Flet client from {archive_path} to {temp_extract}")
    try:
        # Use the artifact name (not archive_path which may have a random suffix
        # from __download_flet_client) to determine the archive format.
        if artifact.endswith(".zip"):
            with zipfile.ZipFile(archive_path, "r") as zf:
                safe_zip_extractall(zf, str(temp_extract))
        else:
            with tarfile.open(archive_path, "r:gz") as tar_arch:
                safe_tar_extractall(tar_arch, str(temp_extract))

        try:
            temp_extract.rename(cache_dir)
        except OSError:
            # Lost a race against a concurrent extraction of the same
            # archive; the winner's cache dir is equivalent.
            if not cache_dir.exists():
                raise
            logger.info(f"Using concurrently extracted cache: {cache_dir}")
            shutil.rmtree(temp_extract, ignore_errors=True)
    except Exception:
        shutil.rmtree(temp_extract, ignore_errors=True)
        raise

    with contextlib.suppress(OSError):
        (cache_dir / ".last-used").touch()
    if fingerprint:
        __gc_stale_client_dirs(cache_dir)
    return cache_dir


def find_macos_app_bundle(directory) -> Path | None:
    """
    Returns the first `.app` bundle directly inside `directory`.

    Args:
        directory: Directory to look in. It need not exist.

    Returns:
        Path to the bundle, or `None` when the directory is missing or holds
            no `.app` — which lets a caller fall through to the next client
            source instead of raising from a directory listing.
    """
    path = Path(directory)
    if not path.is_dir():
        return None

    for name in sorted(os.listdir(path)):
        if name.endswith(".app"):
            return path.joinpath(name)
    return None


def __log_build_client(build_dir: str, client_path: str | Path) -> None:
    """
    Reports that a client from a previous `flet build` is used instead of the
    standard one.

    Logged as a warning, so it is shown even without `flet run -v`: a client
    built before an extension was added lacks that extension, and the app's
    calls to it then time out without pointing at the client.

    Args:
        build_dir: The `build/<platform>` directory the client was found in.
        client_path: The client executable or `.app` bundle that is launched.
    """
    logger.warning(
        f"Using the Flet client from a previous `flet build`: {client_path}. "
        f"Move, rename or delete {build_dir} to use the standard client."
    )


def __linux_identity_args(args: list) -> tuple:
    """
    Give the client window a per-app identity on Linux, without touching it.

    The shipped client is one prebuilt binary called `flet`, so every packed
    app arrives at the taskbar as "flet" -- grouped together, labelled wrong
    and unable to match a desktop entry of its own.

    It does not have to be rebuilt to fix that. GLib takes `prgname` from
    `basename(argv[0])` inside `g_application_run`, and GTK derives the X11
    `WM_CLASS` and the Wayland `app_id` from `prgname` -- so launching the
    same binary under a different `argv[0]` is enough, with `executable`
    still pointing at the real file.

    Args:
        args: Launch argv, whose first element is the client binary path.

    Returns:
        A tuple of the argv to launch and the extra keyword arguments to
        pass to `Popen`. Both are unchanged on every other platform, and
        whenever `FLET_APP_ID` is unset or unusable.
    """

    app_id = os.environ.get("FLET_APP_ID", "").strip()
    if not is_linux() or not app_id or not args:
        return args, {}

    # GLib basenames argv[0], so a path would silently become its last
    # segment; mutter replaces an app id that is not valid UTF-8 with an
    # empty string. Neither is worth guessing about -- keep "flet".
    if "/" in app_id or any(ord(c) < 32 for c in app_id):
        logger.warning(
            f"Ignoring FLET_APP_ID with a path separator or control "
            f"character: {app_id!r}"
        )
        return args, {}
    try:
        app_id.encode("utf-8")
    except UnicodeEncodeError:
        logger.warning(f"Ignoring FLET_APP_ID that is not valid UTF-8: {app_id!r}")
        return args, {}

    executable = str(args[0])
    logger.info(f"Launching the Flet client as {app_id!r} (binary: {executable})")
    return [app_id, *args[1:]], {"executable": executable}


def open_flet_view(page_url, assets_dir, hidden, *, no_impeller=False, app_dir=None):
    """
    Start a desktop view process and return the process object and PID file path.

    Args:
        page_url: Page endpoint the desktop client should open.
        assets_dir: Optional assets directory passed to the client process.
        hidden: Whether the window should start hidden.
        no_impeller: Whether the client renders with Skia instead of Impeller.
        app_dir: Directory of the app's main script, searched for imports of
            extensions the client lacks. Defaults to the directory of
            `sys.argv[0]`.

    Returns:
        A tuple containing:
            - `subprocess.Popen`: started desktop process.
            - `str`: path to a temporary PID file used by `close_flet_view()`.
    """

    args, flet_env, pid_file = __locate_and_unpack_flet_view(
        page_url, assets_dir, hidden, no_impeller, app_dir
    )
    args, extra = __linux_identity_args(args)
    p = subprocess.Popen(args, env=flet_env, **extra)
    __apply_taskbar_props(p.pid)
    return p, pid_file


async def open_flet_view_async(
    page_url, assets_dir, hidden, *, no_impeller=False, app_dir=None
):
    """
    Asynchronously start a desktop view process.

    Args:
        page_url: Page endpoint the desktop client should open.
        assets_dir: Optional assets directory passed to the client process.
        hidden: Whether the window should start hidden.
        no_impeller: Whether the client renders with Skia instead of Impeller.
        app_dir: Directory of the app's main script, searched for imports of
            extensions the client lacks. Defaults to the directory of
            `sys.argv[0]`.

    Returns:
        A tuple containing:
            - `asyncio.subprocess.Process`: started desktop process.
            - `str`: path to a temporary PID file used by `close_flet_view()`.
    """

    args, flet_env, pid_file = __locate_and_unpack_flet_view(
        page_url, assets_dir, hidden, no_impeller, app_dir
    )
    args, extra = __linux_identity_args(args)
    p = await asyncio.create_subprocess_exec(args[0], *args[1:], env=flet_env, **extra)
    __apply_taskbar_props(p.pid)
    return p, pid_file


def explain_client_exit(returncode: int | None) -> None:
    """
    Log a hint when the dynamic loader could not start the desktop client.

    On Linux the dynamic loader exits with status 127 when a shared library the
    client links against is missing or too old, and prints a one-line error that
    names only the library. With the full flavor, the usual cause is `libmpv` or
    GStreamer, which only that flavor links.

    Args:
        returncode: Exit status of the client process, or `None` if it is
            still running.
    """

    if returncode != 127 or not is_linux():
        return
    message = (
        "The Flet desktop client could not start because a library it needs "
        "could not be loaded (see the loader error above)."
    )
    if __get_desktop_flavor() == "full":
        message += (
            " The full client needs libmpv and GStreamer: on Debian 12+ and "
            "Ubuntu 24.04+ run `sudo apt install libmpv2 "
            "libgstreamer-plugins-base1.0-0` (libmpv1 on older releases). Apps "
            "that need none of the extensions only the full client includes can "
            "use the light client by setting FLET_DESKTOP_FLAVOR=light. See "
            "https://flet.dev/docs/getting-started/installation#linux"
        )
    else:
        message += " Install the system package that provides it."
    logger.error(message)


def __apply_taskbar_props(pid: int) -> None:
    """
    Stamp Windows taskbar identity properties on the client window, so packed
    apps (which set `FLET_APP_USER_MODEL_ID` via the PyInstaller runtime hook)
    get their own taskbar name/icon and working pins. No-op elsewhere.

    Args:
        pid: Process ID of the started desktop client.
    """

    if not is_windows() or not os.environ.get("FLET_APP_USER_MODEL_ID"):
        return
    try:
        from flet_desktop.win_taskbar import apply_relaunch_props_async

        apply_relaunch_props_async(pid)
    except Exception as e:
        logger.warning(f"Failed to apply taskbar relaunch properties: {e}")


def close_flet_view(pid_file):
    """
    Terminate a running desktop view process using its PID file.

    The function attempts to read the process ID from `pid_file`, send a
    termination signal, and remove the PID file. Failures while terminating are
    intentionally ignored, but the PID file is removed when possible.

    Args:
        pid_file: Path to the PID file returned by `open_flet_view()`
            or `open_flet_view_async()`.
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


def __locate_and_unpack_flet_view(
    page_url, assets_dir, hidden, no_impeller=False, app_dir=None
):
    """
    Resolve desktop client executable, prepare launch arguments, and environment.

    Resolution strategy (per platform):

    1. Prefer app binaries produced by `flet build` in the current workspace.
    2. Use `FLET_VIEW_PATH` when provided.
    3. Use cached / downloaded client from `~/.flet/client/`, warning about
       the extensions the app uses that it doesn't include.

    Platform-specific launch commands are prepared for Windows, macOS, and Linux.

    Args:
        page_url: Page endpoint the desktop client should open.
        assets_dir: Optional assets directory passed to the client process.
        hidden: Whether to set `FLET_HIDE_WINDOW_ON_START=true` in process env.
        no_impeller: Whether to set `FLET_NO_IMPELLER=true` in process env.
        app_dir: Directory of the app's main script, searched for imports of
            extensions a cached client lacks, or `None` for that of
            `sys.argv[0]`.

    Returns:
        A tuple containing:
            - `list[str]`: command arguments for the desktop client.
            - `dict[str, str]`: environment variables for the launched process.
            - `str`: path to the temporary PID file.

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
            if flet_path:
                __log_build_client(build_windows, flet_path)

        # 2. Check FLET_VIEW_PATH (developer mode)
        if not flet_path:
            flet_view_path = os.environ.get("FLET_VIEW_PATH")
            if flet_view_path and os.path.exists(flet_view_path):
                exe_path = os.path.join(flet_view_path, "flet.exe")
                if os.path.isfile(exe_path):
                    logger.info(f"Flet View found via FLET_VIEW_PATH: {flet_view_path}")
                    flet_path = exe_path
                else:
                    logger.warning(
                        f"FLET_VIEW_PATH set to {flet_view_path} "
                        f"but flet.exe not found there"
                    )

        # 3. Use cached or downloaded client
        if not flet_path:
            cache_dir = ensure_client_cached()
            flet_path = str(cache_dir.joinpath("flet", "flet.exe"))
            __warn_missing_extensions(
                cache_dir, cache_dir.joinpath("flet", "data", "app.so"), app_dir
            )

        args = [flet_path, page_url, pid_file]

    elif is_macos():
        # 1. Try loading Flet client built with the latest run of `flet build`
        build_macos = os.path.join(os.getcwd(), "build", "macos")
        app_path = find_macos_app_bundle(build_macos)
        if app_path:
            __log_build_client(build_macos, app_path)

        # 2. Check FLET_VIEW_PATH (developer mode)
        if not app_path:
            flet_view_path = os.environ.get("FLET_VIEW_PATH")
            if flet_view_path:
                app_path = find_macos_app_bundle(flet_view_path)
                if app_path:
                    logger.info(f"Flet.app is set via FLET_VIEW_PATH: {flet_view_path}")
                else:
                    logger.warning(
                        f"FLET_VIEW_PATH set to {flet_view_path} "
                        f"but no .app bundle found there"
                    )

        # 3. Use cached or downloaded client
        if not app_path:
            temp_flet_dir = ensure_client_cached()
            app_path = find_macos_app_bundle(temp_flet_dir)
            if not app_path:
                raise FileNotFoundError(
                    f"Application bundle not found in {temp_flet_dir}"
                )
            __warn_missing_extensions(
                temp_flet_dir,
                Path(app_path, "Contents", "Frameworks", "App.framework", "App"),
                app_dir,
            )

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
            if app_path:
                __log_build_client(build_linux, app_path)

        # 2. Check FLET_VIEW_PATH (developer mode)
        if not app_path:
            flet_view_path = os.environ.get("FLET_VIEW_PATH")
            if flet_view_path:
                exe_path = str(Path(flet_view_path).joinpath("flet"))
                if os.path.isfile(exe_path):
                    logger.info(
                        f"Flet View is set via FLET_VIEW_PATH: {flet_view_path}"
                    )
                    app_path = exe_path
                else:
                    logger.warning(
                        f"FLET_VIEW_PATH set to {flet_view_path} "
                        f"but flet executable not found there"
                    )
            if not app_path:
                # 3. Use cached or downloaded client
                cache_dir = ensure_client_cached()
                app_path = str(cache_dir.joinpath("flet", "flet"))
                __warn_missing_extensions(
                    cache_dir, cache_dir.joinpath("flet", "lib", "libapp.so"), app_dir
                )

        args = [str(app_path), page_url, pid_file]

    flet_env = {**os.environ}

    if assets_dir:
        args.append(assets_dir)

    if hidden:
        flet_env["FLET_HIDE_WINDOW_ON_START"] = "true"

    if no_impeller:
        flet_env["FLET_NO_IMPELLER"] = "true"

    return args, flet_env, pid_file
