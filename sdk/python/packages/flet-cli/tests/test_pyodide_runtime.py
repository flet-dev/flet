"""The Pyodide runtime bundled with `--no-cdn` builds, `flet publish` and flet-web."""

import io
import json
import tarfile
import zipfile
from pathlib import Path

import pytest

from flet_cli.utils import pyodide

VERSION = "314.0.7"
PYC_URL = f"https://cdn.jsdelivr.net/pyodide/v{VERSION}/pyc/python_stdlib.zip"
WORKERS = [
    Path(__file__).resolve().parents[5] / "client" / "web" / "python-worker.js",
    Path(__file__).resolve().parents[3]
    / "templates"
    / "build"
    / "{{cookiecutter.out_dir}}"
    / "web"
    / "python-worker.js",
]


def _stdlib(compiled: bool) -> bytes:
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as zf:
        zf.writestr("json/__init__.pyc" if compiled else "json/__init__.py", b"x")
    return buffer.getvalue()


def _write_runtime(directory: Path, version: str = VERSION, compiled: bool = True):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "pyodide-lock.json").write_text(
        json.dumps({"info": {"version": version}, "packages": {}})
    )
    (directory / "python_stdlib.zip").write_bytes(_stdlib(compiled))


class TestCacheMatches:
    """`_cache_matches_version()` wanting the precompiled standard library."""

    def test_precompiled_runtime_of_the_version(self, tmp_path):
        _write_runtime(tmp_path)
        assert pyodide._cache_matches_version(tmp_path, VERSION)

    def test_source_standard_library_is_out_of_date(self, tmp_path):
        """A cache made before the precompiled standard library is refreshed."""
        _write_runtime(tmp_path, compiled=False)
        assert not pyodide._cache_matches_version(tmp_path, VERSION)

    def test_other_version_or_missing_files(self, tmp_path):
        _write_runtime(tmp_path, version="314.0.6")
        assert not pyodide._cache_matches_version(tmp_path, VERSION)
        assert not pyodide._cache_matches_version(tmp_path / "missing", VERSION)
        (tmp_path / "python_stdlib.zip").write_bytes(b"not a zip")
        assert not pyodide._cache_matches_version(tmp_path, "314.0.6")


@pytest.fixture
def downloads(monkeypatch, tmp_path):
    """Fake downloads: the core tarball with the source standard library, and
    the precompiled one from the CDN."""
    urls = []

    def download(url, dest, progress, description):
        urls.append(url)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if url.endswith(".tar.bz2"):
            with tarfile.open(dest, "w:bz2") as tf:
                for name, data in (
                    (
                        "pyodide/pyodide-lock.json",
                        json.dumps(
                            {
                                "info": {"version": VERSION},
                                "packages": {
                                    "micropip": {
                                        "name": "micropip",
                                        "file_name": "micropip-0.11.1-py3-none-any.whl",
                                    }
                                },
                            }
                        ).encode(),
                    ),
                    ("pyodide/python_stdlib.zip", _stdlib(compiled=False)),
                    ("pyodide/pyodide.mjs", b"//"),
                ):
                    info = tarfile.TarInfo(name)
                    info.size = len(data)
                    tf.addfile(info, io.BytesIO(data))
        elif url == PYC_URL:
            dest.write_bytes(_stdlib(compiled=True))
        else:
            dest.write_bytes(b"wheel")

    monkeypatch.setattr(pyodide, "_download", download)
    monkeypatch.setattr(pyodide, "_flet_cache_root", lambda: tmp_path / "cache")
    return urls


class TestEnsurePyodide:
    """`ensure_pyodide()` bundling the precompiled standard library."""

    def test_bundle_has_the_precompiled_standard_library(self, downloads, tmp_path):
        dest = tmp_path / "web" / "pyodide"

        pyodide.ensure_pyodide(VERSION, dest)

        assert PYC_URL in downloads
        assert pyodide._stdlib_is_compiled(dest)
        assert (dest / "pyodide.mjs").exists()
        assert (dest / "micropip-0.11.1-py3-none-any.whl").exists()

    def test_refreshes_a_bundle_and_cache_with_sources(self, downloads, tmp_path):
        """Both were made before: the source standard library is replaced."""
        _write_runtime(tmp_path / "cache" / VERSION, compiled=False)
        dest = tmp_path / "web" / "pyodide"
        _write_runtime(dest, compiled=False)

        pyodide.ensure_pyodide(VERSION, dest)

        assert PYC_URL in downloads
        assert pyodide._stdlib_is_compiled(dest)

    def test_up_to_date_bundle_downloads_nothing(self, downloads, tmp_path):
        dest = tmp_path / "web" / "pyodide"
        _write_runtime(dest)

        pyodide.ensure_pyodide(VERSION, dest)

        assert downloads == []


class TestWorker:
    """The web workers loading Pyodide."""

    def test_workers_are_the_same(self):
        """The build template's worker is a copy of the web client's."""
        assert WORKERS[0].read_text() == WORKERS[1].read_text()

    def test_cdn_runtime_loads_the_precompiled_standard_library(self):
        worker = WORKERS[0].read_text()
        assert "...pycStdLib(self.pyodideUrl)," in worker
        assert '"/pyc/python_stdlib.zip"' in worker
