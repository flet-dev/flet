import gzip
import hashlib
import json
import logging
import os
import shutil
import tarfile
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Optional

from flet.utils import copy_tree, is_macos, is_windows
from flet_desktop import (
    ensure_client_cached,
    find_macos_app_bundle,
    get_artifact_filename,
)

logger = logging.getLogger(__name__)


def get_flet_bin_path() -> Optional[str]:
    """
    Return path to Flet desktop binaries, if available.

    Resolution order:

    1. FLET_VIEW_PATH environment variable.
    2. Cached / downloaded client from ~/.flet/client/.

    Returns:
        Absolute binaries directory path or `None` when not found.
    """

    # 1. Check FLET_VIEW_PATH (developer / custom build mode).
    flet_view_path = os.environ.get("FLET_VIEW_PATH")
    if flet_view_path and os.path.exists(flet_view_path):
        return flet_view_path

    # 2. Fall back to cached / downloaded client.
    cache_dir = ensure_client_cached()
    if cache_dir and cache_dir.exists():
        return str(cache_dir)

    return None


def normalize_tar_entry(tarinfo: tarfile.TarInfo) -> tarfile.TarInfo:
    """
    Normalize a tar entry's metadata (mtime, owner) so that archives built
    from identical content are byte-identical across builds.

    Args:
        tarinfo: Entry to normalize, as passed by `tarfile.TarFile.add`.

    Returns:
        The same entry, with mtime and ownership zeroed.
    """

    tarinfo.mtime = 0
    tarinfo.uid = tarinfo.gid = 0
    tarinfo.uname = tarinfo.gname = ""
    return tarinfo


def resolve_flet_client() -> Optional[tuple[str, str]]:
    """
    Find the Flet desktop client to bundle with the app.

    The cached client keeps the client in a `flet` subdirectory, while
    `FLET_VIEW_PATH` may name the client directory itself. The client must
    hold its executable (`flet.exe` on Windows, `flet` on Linux, a `.app`
    bundle on macOS): the app trusts a bundled archive and doesn't download
    the client, so an archive without one would fail on every start.

    Returns:
        `(client_dir, arcname)`: the client directory, and its name in the
            client archive (`flet`, or the `.app` bundle name on macOS). `None`
            when no client is available.

    Raises:
        RuntimeError: If the client directory holds no client executable.
    """

    bin_path = get_flet_bin_path()
    if not bin_path:
        return None

    if bin_path == os.environ.get("FLET_VIEW_PATH"):
        source = f"FLET_VIEW_PATH ({bin_path})"
        hint = "Point FLET_VIEW_PATH at a Flet client directory, or unset it."
    else:
        source = f"The cached Flet client ({bin_path})"
        hint = "Delete that directory and try again."

    if is_macos():
        app_path = find_macos_app_bundle(bin_path)
        if app_path is None:
            raise RuntimeError(f"{source} holds no .app bundle. {hint}")
        return str(app_path), app_path.name

    client_dir = os.path.join(bin_path, "flet")
    src_dir = client_dir if os.path.isdir(client_dir) else bin_path
    exe = "flet.exe" if is_windows() else "flet"
    if not os.path.isfile(os.path.join(src_dir, exe)):
        raise RuntimeError(f"{source} holds no {exe}. {hint}")
    return src_dir, "flet"


def get_linux_client_flavor(client_dir: str) -> str:
    """
    Return the flavor of the Linux client in `client_dir`: `"full"` or
    `"light"`.

    Only the full client includes `media_kit`, which links the `libmpv` of the
    distro it was built on. The runtime runs a light client on any distro with
    a new enough glibc, so a client is called light only when it lacks
    `media_kit`.

    Args:
        client_dir: Linux client directory, holding `lib/`.
    """

    try:
        libs = os.listdir(os.path.join(client_dir, "lib"))
    except OSError:
        libs = []
    return "full" if any(lib.startswith("libmedia_kit") for lib in libs) else "light"


def get_client_archive_name(client_dir: str) -> Optional[str]:
    """
    Return the name the runtime looks for the client archive under.

    On Linux the name holds the flavor of the client in `client_dir`, rather
    than the configured one, since `FLET_VIEW_PATH` may point at either.

    Args:
        client_dir: Client directory to archive.

    Returns:
        The archive name, or `None` when no client archive can be named for
            this Linux system: the runtime couldn't pick a client here either.
    """

    if is_windows() or is_macos():
        return get_artifact_filename()
    try:
        return get_artifact_filename(get_linux_client_flavor(client_dir))
    except RuntimeError as e:
        logger.warning(f"Not bundling the Flet client: {e}")
        return None


def copy_flet_bin() -> Optional[str]:
    """
    Copy the Flet desktop client into a new temporary directory.

    `flet pack` customizes the copy, then archives it with
    `stage_client_archive()`. The copy holds only the client, as
    `<temp dir>/<arcname>`, whichever layout it was found in.

    Returns:
        Path to the temporary directory, or `None` when no client is
            available.

    Raises:
        RuntimeError: If the client directory holds no client executable.
    """

    client = resolve_flet_client()
    if not client:
        return None
    src_dir, arcname = client
    temp_bin_dir = Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    copy_tree(src_dir, str(temp_bin_dir.joinpath(arcname)))
    return str(temp_bin_dir)


def write_client_archive(src_dir: str, arcname: str, archive_path: str) -> None:
    """
    Write `src_dir` into a client archive under the top-level name `arcname`.

    Fixed timestamps and sorted entries make the archive byte-identical for
    identical inputs, so the runtime cache fingerprint (and thus the client
    cache directory) only changes when the content does.

    Args:
        src_dir: Directory to archive.
        arcname: Name of `src_dir` inside the archive, e.g. `flet` or `Flet.app`.
        archive_path: Archive to create: zip for a `.zip` name, gzipped tar
            otherwise.
    """

    if archive_path.endswith(".zip"):
        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(src_dir):
                dirs.sort()
                for f in sorted(files):
                    full = os.path.join(root, f)
                    name = os.path.join(arcname, os.path.relpath(full, src_dir))
                    zi = zipfile.ZipInfo(
                        name.replace(os.sep, "/"), date_time=(1980, 1, 1, 0, 0, 0)
                    )
                    zi.compress_type = zipfile.ZIP_DEFLATED
                    zi.external_attr = (os.stat(full).st_mode & 0xFFFF) << 16
                    with open(full, "rb") as src, zf.open(zi, "w") as dest:
                        shutil.copyfileobj(src, dest)
    else:
        with (
            open(archive_path, "wb") as raw,
            # No file name in the gzip header, which would differ per path.
            gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as gz,
            tarfile.open(fileobj=gz, mode="w") as tar,
        ):
            tar.add(src_dir, arcname=arcname, filter=normalize_tar_entry)


def write_archive_fingerprint(archive_path: str) -> None:
    """
    Write a `<archive>.sha256` sidecar holding `<hash> <size>`.

    `flet_desktop.ensure_client_cached()` uses it at runtime to key the
    client cache directory by content, so a bundled client doesn't collide
    with the downloaded client or other apps' bundled clients. The size lets
    the runtime detect a stale sidecar next to a replaced archive and re-hash
    instead of trusting it.

    Args:
        archive_path: Path of the client archive to fingerprint.
    """

    h = hashlib.sha256()
    with open(archive_path, "rb") as f:
        while chunk := f.read(1024 * 1024):
            h.update(chunk)
    with open(archive_path + ".sha256", "w") as f:
        f.write(f"{h.hexdigest()} {os.path.getsize(archive_path)}")


def _get_source_stamp(src_dir: str, arcname: str, archive_name: str) -> str:
    """
    Return a stamp of the files in `src_dir`, from their names, sizes and
    modification times, to tell cheaply whether an archive of them is current.
    """

    entries = []
    for root, dirs, files in os.walk(src_dir):
        dirs.sort()
        for name in sorted(dirs + files):
            path = os.path.join(root, name)
            st = os.lstat(path)
            entries.append([os.path.relpath(path, src_dir), st.st_size, st.st_mtime_ns])
    data = json.dumps([arcname, archive_name, entries])
    return hashlib.sha256(data.encode()).hexdigest()


def stage_client_archive(
    src_dir: str, arcname: str, archive_name: str, dest_dir: str
) -> list[str]:
    """
    Write the client archive and its fingerprint sidecar into `dest_dir`.

    `dest_dir` must outlive the build: PyInstaller caches the analysis that
    lists these files and reuses it on the next build when nothing it tracks
    has changed, skipping a missing file with only a warning. So the archive
    is replaced only when its content changes, which also tells PyInstaller,
    through the newer modification time, to analyze again. When the files of
    `src_dir` haven't changed since the last call, the archive isn't even
    rebuilt. Other archives left in `dest_dir` are removed.

    Args:
        src_dir: Client directory to archive.
        arcname: Name of `src_dir` inside the archive.
        archive_name: Name of the archive, see `get_client_archive_name()`.
        dest_dir: Directory to write the archive into; created if missing.

    Returns:
        Paths of the archive and its sidecar, the files to bundle.
    """

    dest = Path(dest_dir)
    dest.mkdir(parents=True, exist_ok=True)
    archive = dest / archive_name
    sidecar = dest / f"{archive_name}.sha256"
    stamp_file = dest / ".source"
    files = [str(archive), str(sidecar)]

    stamp = _get_source_stamp(src_dir, arcname, archive_name)
    current = archive.is_file() and sidecar.is_file()
    if current and stamp_file.is_file() and stamp_file.read_text() == stamp:
        return files

    # The extension picks the archive format, so it stays last.
    temp = dest / f".{uuid.uuid4().hex}.{archive_name}"
    temp_sidecar = Path(f"{temp}.sha256")
    try:
        write_client_archive(src_dir, arcname, str(temp))
        write_archive_fingerprint(str(temp))
        if current and sidecar.read_text() == temp_sidecar.read_text():
            # Same content: keep the files, and their modification times.
            temp.unlink()
            temp_sidecar.unlink()
        else:
            os.replace(temp, archive)
            os.replace(temp_sidecar, sidecar)
    finally:
        for path in (temp, temp_sidecar):
            path.unlink(missing_ok=True)

    for entry in dest.iterdir():
        if entry not in (archive, sidecar, stamp_file):
            if entry.is_dir() and not entry.is_symlink():
                shutil.rmtree(entry, ignore_errors=True)
            else:
                entry.unlink(missing_ok=True)
    stamp_file.write_text(stamp)
    return files


def archive_flet_bin(dest_dir: str) -> Optional[list[str]]:
    """
    Pack the Flet desktop client into the archive the app unpacks at runtime.

    `flet_desktop.ensure_client_cached()` looks for this archive in the
    bundled `flet_desktop/app` directory, and downloads the client when it
    isn't there. This is what a plain `pyinstaller` run bundles; `flet pack`
    stages the archive of the client it customizes itself.

    Args:
        dest_dir: Directory to write the archive into, see
            `stage_client_archive()`.

    Returns:
        Paths of the archive and its fingerprint sidecar, or `None` when no
            client is available or can be named for this system.

    Raises:
        RuntimeError: If the client directory holds no client executable.
    """

    client = resolve_flet_client()
    if not client:
        return None
    src_dir, arcname = client
    archive_name = get_client_archive_name(src_dir)
    if not archive_name:
        return None
    return stage_client_archive(src_dir, arcname, archive_name, dest_dir)
