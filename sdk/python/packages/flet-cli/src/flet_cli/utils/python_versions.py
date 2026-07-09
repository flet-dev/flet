"""Supported Python versions for `flet build` / `flet publish`.

The set of bundlable Python releases — and the matching CPython-standalone +
Pyodide artifacts — is defined by python-build's date-keyed ``manifest.json``,
the single source of truth shared with serious_python. This module pins one
python-build release date and fetches that release's manifest (cached under
``~/.flet/cache``, immutable per date), so nothing here is hand-mirrored.

Pin (``PYTHON_BUILD_RELEASE_DATE``) overrides, for dev/CI:
* ``FLET_PYTHON_BUILD_RELEASE_DATE`` — use a different published release date.
* ``FLET_PYTHON_BUILD_MANIFEST`` — read a local ``manifest.json`` instead of
  fetching (mirrors serious_python's ``gen_version_tables --manifest``).
"""

import json
import os
import shutil
import urllib.request
from dataclasses import dataclass
from functools import lru_cache
from typing import Callable, Optional

from packaging.specifiers import SpecifierSet
from packaging.version import Version

from flet_cli.utils.template_cache import get_cache_root

# python-build release this flet pins. Keep in sync with serious_python's
# `pythonReleaseDate` (lib/src/python_versions.dart) — both should track the
# same python-build release.
PYTHON_BUILD_RELEASE_DATE = "20260708"

RELEASE_DATE_ENV = "FLET_PYTHON_BUILD_RELEASE_DATE"
MANIFEST_PATH_ENV = "FLET_PYTHON_BUILD_MANIFEST"

_MANIFEST_URL = (
    "https://github.com/flet-dev/python-build/releases/download/{date}/manifest.json"
)


@dataclass(frozen=True)
class PythonRelease:
    short: str
    standalone: str
    pyodide: str
    # Android ABIs python-build publishes distributions for this minor
    # (per the manifest's per-minor `android_abis`).
    android_abis: tuple[str, ...]
    # When True, this release is supported via `--python-version` (and an
    # explicit `requires-python = "==X.Y.*"` specifier) but is not picked
    # automatically by the default or by open-ended `requires-python`
    # specifiers like `>=3.14`. Use for beta CPython lines.
    prerelease: bool


def _resolve_release_date() -> str:
    return os.environ.get(RELEASE_DATE_ENV) or PYTHON_BUILD_RELEASE_DATE


def _load_manifest() -> dict:
    """Return the python-build manifest as a dict.

    Reads ``$FLET_PYTHON_BUILD_MANIFEST`` if set; otherwise fetches the pinned
    release's ``manifest.json`` (cached immutably under
    ``~/.flet/cache/python-build``). Falls back to a present cache when the
    network is unavailable; raises with an actionable message if neither the
    network nor a cache can supply it.
    """
    local = os.environ.get(MANIFEST_PATH_ENV)
    if local:
        with open(local, encoding="utf-8") as f:
            return json.load(f)

    date = _resolve_release_date()
    url = _MANIFEST_URL.format(date=date)
    cache_path = get_cache_root() / "python-build" / f"manifest-{date}.json"

    if not (cache_path.exists() and cache_path.stat().st_size > 0):
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = cache_path.with_suffix(cache_path.suffix + ".tmp")
        try:
            with urllib.request.urlopen(url) as resp, open(tmp_path, "wb") as out:
                shutil.copyfileobj(resp, out)
                out.flush()
                os.fsync(out.fileno())
            os.replace(tmp_path, cache_path)
        except BaseException as e:
            tmp_path.unlink(missing_ok=True)
            if not (cache_path.exists() and cache_path.stat().st_size > 0):
                raise RuntimeError(
                    f"Could not obtain the Python build manifest for release "
                    f"{date} from {url}: {e}. Check your network connection, or "
                    f"set ${MANIFEST_PATH_ENV} to a local manifest.json."
                ) from e

    with cache_path.open(encoding="utf-8") as f:
        return json.load(f)


@lru_cache(maxsize=1)
def _load_data() -> tuple[tuple[PythonRelease, ...], str]:
    manifest = _load_manifest()
    releases = tuple(
        PythonRelease(
            short=short,
            standalone=info["full_version"],
            pyodide=info["pyodide_version"],
            android_abis=tuple(info["android_abis"]),
            prerelease=bool(info.get("prerelease", False)),
        )
        for short, info in manifest["pythons"].items()
    )
    return releases, manifest["default_python_version"]


def get_supported_python_versions() -> list[PythonRelease]:
    return list(_load_data()[0])


def get_default_python_version() -> str:
    return _load_data()[1]


def get_release(short: str) -> Optional[PythonRelease]:
    for r in get_supported_python_versions():
        if r.short == short:
            return r
    return None


def supported_short_versions() -> list[str]:
    return [r.short for r in get_supported_python_versions()]


class UnsupportedPythonVersionError(ValueError):
    pass


def resolve_python_version(
    cli_arg: Optional[str],
    get_pyproject: Optional[Callable[[Optional[str]], object]] = None,
) -> PythonRelease:
    """Resolve the Python release to bundle.

    Priority: `--python-version` CLI arg → `[project].requires-python` (parsed
    as a PEP 440 SpecifierSet, highest matching supported short version wins) →
    the manifest's default.

    Raises `UnsupportedPythonVersionError` if the CLI arg names an unsupported
    version, or if `requires-python` excludes every supported version.
    """

    supported = get_supported_python_versions()

    if cli_arg:
        release = get_release(cli_arg)
        if release is None:
            raise UnsupportedPythonVersionError(
                f"Unsupported Python version: {cli_arg!r}. "
                f"Supported: {', '.join(supported_short_versions())}."
            )
        return release

    if get_pyproject is not None:
        requires = get_pyproject("project.requires-python")
        if isinstance(requires, str) and requires.strip():
            try:
                spec = SpecifierSet(requires)
            except Exception:
                spec = None
            if spec is not None:
                # Prefer the highest stable row that satisfies the
                # specifier, matched against the full standalone version so
                # e.g. `>=3.13` matches the 3.13.x row, not just
                # `Version("3.13")`. Pre-release rows are skipped here so
                # `>=3.14` never silently jumps to a beta CPython line.
                stable_matching = [
                    r
                    for r in supported
                    if not r.prerelease and Version(r.standalone) in spec
                ]
                if stable_matching:
                    return max(stable_matching, key=lambda r: Version(r.standalone))

                # Fall back: match pre-release rows against the short
                # version (e.g. `3.15`) rather than the standalone (e.g.
                # `3.15.0a2`). Without this, `>=3.15` would skip the 3.15
                # alpha because `3.15.0a2` sorts before `3.15.0`. Comparing
                # by short version expresses "this Python line is supported"
                # — which is what the registry represents — and preserves
                # the "explicit opt-in" path for beta lines without exposing
                # a CLI flag.
                spec_with_pre = SpecifierSet(requires, prereleases=True)
                prerelease_matching = [
                    r
                    for r in supported
                    if r.prerelease and Version(r.short) in spec_with_pre
                ]
                if prerelease_matching:
                    return max(
                        prerelease_matching,
                        key=lambda r: Version(r.short),
                    )

                raise UnsupportedPythonVersionError(
                    f"`requires-python = {requires!r}` does not match any "
                    f"supported Python version "
                    f"({', '.join(supported_short_versions())})."
                )

    fallback = get_release(get_default_python_version())
    assert fallback is not None
    return fallback
