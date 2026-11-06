import gzip
import hashlib
import os
import shutil
import tarfile
import tempfile
import uuid
import zipfile
from pathlib import Path
from typing import Optional

from flet.utils import copy_tree, is_macos
from flet_desktop import (
    ensure_client_cached,
    find_macos_app_bundle,
    get_artifact_filename,
)


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


def copy_flet_bin() -> Optional[str]:
    """
    Copy packaged Flet desktop binaries into a temporary directory.

    Returns:
        Path to the temporary copied binaries directory, or `None` when source
        binaries are unavailable.
    """

    bin_path = get_flet_bin_path()
    if not bin_path:
        return None

    # create temp bin dir
    temp_bin_dir = Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    copy_tree(bin_path, str(temp_bin_dir))
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
            gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz,
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


def archive_flet_bin() -> Optional[str]:
    """
    Pack the Flet desktop client into the archive the app unpacks at runtime.

    `flet_desktop.ensure_client_cached()` looks for this archive, named after
    `flet_desktop.get_artifact_filename()`, in the bundled `flet_desktop/app`
    directory, and downloads the client when it isn't there. This is what a
    plain `pyinstaller` run bundles; `flet pack` builds its own archive from
    the client it customizes.

    Returns:
        Path to a new temporary directory holding only the archive and its
            fingerprint sidecar, or `None` when no client is available.
    """

    bin_path = get_flet_bin_path()
    if not bin_path:
        return None

    if is_macos():
        app_path = find_macos_app_bundle(bin_path)
        if app_path is None:
            return None
        src_dir, arcname = str(app_path), app_path.name
    else:
        # The cached client keeps it in a `flet` subdirectory, while
        # `FLET_VIEW_PATH` names the client directory itself.
        client_dir = os.path.join(bin_path, "flet")
        src_dir = client_dir if os.path.isdir(client_dir) else bin_path
        arcname = "flet"

    temp_dir = Path(tempfile.gettempdir()).joinpath(str(uuid.uuid4()))
    temp_dir.mkdir()
    archive_path = str(temp_dir.joinpath(get_artifact_filename()))
    write_client_archive(src_dir, arcname, archive_path)
    write_archive_fingerprint(archive_path)
    return str(temp_dir)
