"""Download + cache the Pyodide runtime that matches a Python release.

`pyodide-core-<version>.tar.bz2` carries the runtime (pyodide.js / asm.wasm /
python_stdlib.zip / pyodide-lock.json / ...) but not the micropip+packaging
wheels that `loadPackage("micropip")` needs at runtime. We supplement the core
tarball with those two wheels (filenames resolved from pyodide-lock.json) so
the bundle works in `--no-cdn` deployments too.

Its `python_stdlib.zip` is replaced with the precompiled one Pyodide publishes
on its CDN (`pyc/python_stdlib.zip`): `.pyc` files instead of sources, so
Python doesn't compile the modules it imports when the app starts.
"""

from __future__ import annotations

import json
import shutil
import tarfile
import zipfile
from collections.abc import Iterable
from pathlib import Path

from rich.progress import Progress

from flet_cli.utils.distros import download_with_progress
from flet_cli.utils.template_cache import get_cache_root

_GITHUB_TARBALL_URL = "https://github.com/pyodide/pyodide/releases/download/{version}/pyodide-core-{version}.tar.bz2"
_CDN_FILE_URL = "https://cdn.jsdelivr.net/pyodide/v{version}/full/{filename}"
_CDN_PYC_STDLIB_URL = (
    "https://cdn.jsdelivr.net/pyodide/v{version}/pyc/python_stdlib.zip"
)
_STDLIB = "python_stdlib.zip"

# Wheels that pyodide loads from disk/CDN at runtime via loadPackage().
# Without them in dest_dir, `--no-cdn` builds break.
_EXTRA_RUNTIME_PACKAGES = ("micropip", "packaging")


def _flet_cache_root() -> Path:
    return get_cache_root() / "pyodide"


def _download(url: str, dest: Path, progress: Progress, description: str) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    download_with_progress(url, str(dest), progress, description=description)


def _resolve_runtime_wheel_filenames(
    lock_json: Path, package_names: Iterable[str]
) -> list[str]:
    with lock_json.open("r", encoding="utf-8") as f:
        lock = json.load(f)
    wanted = set(package_names)
    filenames: list[str] = []
    for pkg in lock.get("packages", {}).values():
        name = pkg.get("name")
        fn = pkg.get("file_name")
        if name in wanted and isinstance(fn, str) and fn.endswith(".whl"):
            filenames.append(fn)
    return filenames


def _populate_cache(version: str, cache_dir: Path) -> None:
    """Fetch core tarball + supplementary wheels into `cache_dir`."""

    cache_dir.mkdir(parents=True, exist_ok=True)
    tarball = cache_dir / f"pyodide-core-{version}.tar.bz2"

    with Progress(transient=True) as progress:
        _download(
            _GITHUB_TARBALL_URL.format(version=version),
            tarball,
            progress,
            f"Downloading Pyodide {version}...",
        )
    with tarfile.open(tarball, "r:bz2") as tf:
        # The core tarball nests everything under a top-level "pyodide/" dir.
        # Strip that prefix as we extract so files land directly in cache_dir.
        for member in tf.getmembers():
            if member.isdir():
                continue
            rel = Path(member.name)
            if rel.parts and rel.parts[0] == "pyodide":
                rel = Path(*rel.parts[1:])
            if not rel.parts:
                continue
            target = cache_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            extracted = tf.extractfile(member)
            if extracted is None:
                continue
            with extracted as src, target.open("wb") as dst:
                shutil.copyfileobj(src, dst)
    tarball.unlink(missing_ok=True)

    lock_json = cache_dir / "pyodide-lock.json"
    if not lock_json.exists():
        raise RuntimeError(f"pyodide-core-{version} did not contain pyodide-lock.json")
    with Progress(transient=True) as progress:
        _download(
            _CDN_PYC_STDLIB_URL.format(version=version),
            cache_dir / _STDLIB,
            progress,
            "Downloading precompiled Python standard library...",
        )
        for wheel in _resolve_runtime_wheel_filenames(
            lock_json, _EXTRA_RUNTIME_PACKAGES
        ):
            wheel_path = cache_dir / wheel
            if wheel_path.exists():
                continue
            _download(
                _CDN_FILE_URL.format(version=version, filename=wheel),
                wheel_path,
                progress,
                f"Downloading {wheel}...",
            )


def _stdlib_is_compiled(cache_dir: Path) -> bool:
    """Whether `python_stdlib.zip` holds `.pyc` files and no sources."""
    try:
        with zipfile.ZipFile(cache_dir / _STDLIB) as zf:
            names = zf.namelist()
    except (OSError, zipfile.BadZipFile):
        return False
    return any(n.endswith(".pyc") for n in names) and not any(
        n.endswith(".py") for n in names
    )


def _cache_matches_version(cache_dir: Path, version: str) -> bool:
    if not _stdlib_is_compiled(cache_dir):
        # Missing, or the source standard library of a cache made before the
        # precompiled one.
        return False
    if not (cache_dir / "pyodide-lock.json").exists():
        return False
    return _runtime_version(cache_dir) == version


def _runtime_version(cache_dir: Path) -> str | None:
    """The Pyodide version of a runtime: `package.json`'s `version`, which every
    release has, else `pyodide-lock.json`'s `info.version`, which only 0.27 and
    earlier write."""
    for name, keys in (
        ("package.json", ("version",)),
        ("pyodide-lock.json", ("info", "version")),
    ):
        try:
            with (cache_dir / name).open("r", encoding="utf-8") as f:
                value = json.load(f)
        except (OSError, json.JSONDecodeError):
            continue
        for key in keys:
            value = value.get(key) if isinstance(value, dict) else None
        if isinstance(value, str):
            return value
    return None


def ensure_pyodide(version: str, dest_dir: Path) -> None:
    """Ensure a working Pyodide runtime of `version` exists at `dest_dir`.

    Cached per version under `~/.flet/cache/pyodide/<version>/`. Idempotent: if
    `dest_dir` already has that version with the precompiled standard library, no
    work is done.
    """

    dest_dir = Path(dest_dir)
    if _cache_matches_version(dest_dir, version):
        return

    cache_dir = _flet_cache_root() / version
    if not _cache_matches_version(cache_dir, version):
        # Wipe a partial cache from a prior failed run.
        if cache_dir.exists():
            shutil.rmtree(cache_dir)
        _populate_cache(version, cache_dir)

    dest_dir.mkdir(parents=True, exist_ok=True)
    for src in cache_dir.iterdir():
        if not src.is_file():
            continue
        shutil.copy2(src, dest_dir / src.name)
