"""Tests for manifest-backed Python version resolution.

These run fully offline: `FLET_PYTHON_BUILD_MANIFEST` points the loader at a
local fixture manifest instead of fetching python-build's release asset.
"""

import json

import pytest

from flet_cli.utils import python_versions as pv

_FIXTURE_MANIFEST = {
    "release": "20260614",
    "default_python_version": "3.14",
    "dart_bridge_version": "1.2.3",
    "pythons": {
        "3.12": {
            "full_version": "3.12.13",
            "pyodide_version": "0.27.7",
            "android_abis": ["arm64-v8a", "x86_64", "armeabi-v7a"],
            "prerelease": False,
        },
        "3.13": {
            "full_version": "3.13.14",
            "pyodide_version": "0.29.4",
            "android_abis": ["arm64-v8a", "x86_64"],
            "prerelease": False,
        },
        "3.14": {
            "full_version": "3.14.6",
            "pyodide_version": "314.0.0",
            "android_abis": ["arm64-v8a", "x86_64"],
            "prerelease": False,
        },
        # A pre-release line: opt-in only, never auto-resolved.
        "3.15": {
            "full_version": "3.15.0a1",
            "pyodide_version": "315.0.0",
            "android_abis": ["arm64-v8a", "x86_64"],
            "prerelease": True,
        },
    },
}


@pytest.fixture(autouse=True)
def fixture_manifest(tmp_path, monkeypatch):
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(_FIXTURE_MANIFEST), encoding="utf-8")
    monkeypatch.setenv(pv.MANIFEST_PATH_ENV, str(manifest_path))
    pv._load_data.cache_clear()
    yield
    pv._load_data.cache_clear()


def test_default_and_supported_versions():
    assert pv.get_default_python_version() == "3.14"
    assert pv.supported_short_versions() == ["3.12", "3.13", "3.14", "3.15"]


def test_release_fields_mapped_from_manifest():
    r = pv.get_release("3.14")
    assert r is not None
    assert (r.short, r.standalone, r.pyodide, r.prerelease) == (
        "3.14",
        "3.14.6",
        "314.0.0",
        False,
    )
    assert pv.get_release("3.99") is None


def test_resolve_default_when_no_arg():
    assert pv.resolve_python_version(None).short == "3.14"


def test_resolve_explicit_cli_arg():
    assert pv.resolve_python_version("3.12").short == "3.12"


def test_resolve_unsupported_cli_arg_raises():
    with pytest.raises(pv.UnsupportedPythonVersionError):
        pv.resolve_python_version("3.99")


def test_resolve_from_requires_python_picks_highest_stable():
    get_pyproject = lambda key: ">=3.13"  # noqa: E731
    assert pv.resolve_python_version(None, get_pyproject).short == "3.14"


def test_resolve_from_requires_python_exact():
    get_pyproject = lambda key: "==3.12.*"  # noqa: E731
    assert pv.resolve_python_version(None, get_pyproject).short == "3.12"


def test_requires_python_skips_prerelease_for_open_specifier():
    # `>=3.14` must not silently jump to the 3.15 pre-release line.
    get_pyproject = lambda key: ">=3.14"  # noqa: E731
    assert pv.resolve_python_version(None, get_pyproject).short == "3.14"


def test_requires_python_opts_into_prerelease_explicitly():
    get_pyproject = lambda key: "==3.15.*"  # noqa: E731
    assert pv.resolve_python_version(None, get_pyproject).short == "3.15"


def test_requires_python_no_match_raises():
    get_pyproject = lambda key: ">=3.99"  # noqa: E731
    with pytest.raises(pv.UnsupportedPythonVersionError):
        pv.resolve_python_version(None, get_pyproject)
