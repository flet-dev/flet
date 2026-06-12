"""Supported Python versions for `flet build` / `flet publish`.

This module is the single source of truth on the Python side for which
Python releases the Flet toolchain can bundle, and the matching
CPython-standalone + Pyodide artifacts. Mirror any change here in
serious_python's `_pythonReleases` map (bin/package_command.dart).
"""

from dataclasses import dataclass
from typing import Callable, Optional

from packaging.specifiers import SpecifierSet
from packaging.version import Version


@dataclass(frozen=True)
class PythonRelease:
    short: str
    standalone: str
    standalone_date: str
    # Release date tag of the matching `flet-dev/python-build` release
    # (e.g. "20260611"). Combined with `standalone` to construct the
    # platform-plugin download URLs.
    python_build_date: str
    pyodide: str
    pyodide_platform_tag: str
    # When True, this release is supported via `--python-version` (and an
    # explicit `requires-python = "==X.Y.*"` specifier) but is not picked
    # automatically by the default or by open-ended `requires-python`
    # specifiers like `>=3.14`. Use for beta CPython lines.
    prerelease: bool


SUPPORTED_PYTHON_VERSIONS: list[PythonRelease] = [
    PythonRelease(
        short="3.12",
        standalone="3.12.13",
        standalone_date="20260610",
        python_build_date="20260611",
        pyodide="0.27.7",
        pyodide_platform_tag="pyodide-2024.0-wasm32",
        prerelease=False,
    ),
    PythonRelease(
        short="3.13",
        standalone="3.13.14",
        standalone_date="20260610",
        python_build_date="20260611",
        pyodide="0.29.4",
        pyodide_platform_tag="pyemscripten-2025.0-wasm32",
        prerelease=False,
    ),
    PythonRelease(
        short="3.14",
        standalone="3.14.6",
        standalone_date="20260610",
        python_build_date="20260611",
        pyodide="314.0.0",
        pyodide_platform_tag="pyemscripten-2026.0-wasm32",
        prerelease=False,
    ),
    # Add future pre-release CPython lines with `prerelease=True`. They are
    # opt-in via `--python-version 3.15` or an explicit
    # `requires-python = "==3.15.*"`; never the auto-resolved default.
    #
    # PythonRelease(
    #     short="3.15",
    #     standalone="3.15.0",
    #     standalone_date="...",
    #     python_build_date="...",
    #     pyodide="...",
    #     pyodide_platform_tag="...",
    #     prerelease=True,
    # ),
]

DEFAULT_PYTHON_VERSION = "3.14"


def get_release(short: str) -> Optional[PythonRelease]:
    for r in SUPPORTED_PYTHON_VERSIONS:
        if r.short == short:
            return r
    return None


def supported_short_versions() -> list[str]:
    return [r.short for r in SUPPORTED_PYTHON_VERSIONS]


class UnsupportedPythonVersionError(ValueError):
    pass


def resolve_python_version(
    cli_arg: Optional[str],
    get_pyproject: Optional[Callable[[Optional[str]], object]] = None,
) -> PythonRelease:
    """Resolve the Python release to bundle.

    Priority: `--python-version` CLI arg → `[project].requires-python` (parsed
    as a PEP 440 SpecifierSet, highest matching supported short version wins) →
    `DEFAULT_PYTHON_VERSION`.

    Raises `UnsupportedPythonVersionError` if the CLI arg names an unsupported
    version, or if `requires-python` excludes every supported version.
    """

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
                    for r in SUPPORTED_PYTHON_VERSIONS
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
                    for r in SUPPORTED_PYTHON_VERSIONS
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

    fallback = get_release(DEFAULT_PYTHON_VERSION)
    assert fallback is not None
    return fallback
