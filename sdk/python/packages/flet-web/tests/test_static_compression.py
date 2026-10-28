"""Gzip compression of the static files served for a Flet web app."""

import gzip
import importlib
import os

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

static_files = importlib.import_module("flet_web.fastapi.flet_static_files")

GZIP = {"Accept-Encoding": "gzip"}
WASM = bytes(range(256)) * 4096


@pytest.fixture
def web(tmp_path, monkeypatch):
    """A packaged web client directory with a compressible and a binary file."""
    web = tmp_path / "web"
    web.mkdir()
    (web / "index.html").write_text("<html><head></head><body></body></html>")
    (web / "manifest.json").write_text("{}")
    (web / "main.dart.wasm").write_bytes(WASM)
    (web / "small.js").write_text("main();")
    (web / "logo.png").write_bytes(b"\x89PNG" + bytes(4096))
    monkeypatch.setattr(static_files, "get_package_web_dir", lambda: str(web))
    return web


@pytest.fixture
def client(web):
    """A test client of an app serving `web`."""
    app = FastAPI()
    app.mount("/", static_files.FletStaticFiles())
    with TestClient(app) as client:
        yield client


class TestAcceptsGzip:
    @pytest.mark.parametrize(
        ("accept_encoding", "expected"),
        [
            ("gzip, deflate, br, zstd", True),
            ("GZIP", True),
            ("br;q=1.0, gzip;q=0.5", True),
            ("gzip;q=0", False),
            ("gzip;q=0.0, br", False),
            ("gzip;q=invalid", False),
            ("br, deflate", False),
            ("", False),
            ("*;q=1, identity;q=0", True),
            ("*, gzip;q=0", False),
            ("*;q=0", False),
        ],
    )
    def test_reads_accept_encoding(self, accept_encoding, expected):
        """`gzip`, or else `*`, is accepted when listed without a zero quality."""
        assert static_files.accepts_gzip(accept_encoding) is expected


class TestCompressedResponses:
    def test_sends_gzip_to_browsers_that_accept_it(self, client):
        """A compressible file is sent gzipped with its own media type."""
        response = client.get("/main.dart.wasm", headers=GZIP)

        assert response.status_code == 200
        assert response.headers["content-encoding"] == "gzip"
        assert response.headers["content-type"] == "application/wasm"
        assert response.headers["vary"] == "Accept-Encoding"
        assert int(response.headers["content-length"]) < len(WASM) / 10
        assert response.content == WASM

    def test_sends_plain_file_to_other_browsers(self, client):
        """Without gzip in `Accept-Encoding`, the file is sent as is."""
        response = client.get(
            "/main.dart.wasm", headers={"Accept-Encoding": "identity"}
        )

        assert response.status_code == 200
        assert "content-encoding" not in response.headers
        assert response.headers["vary"] == "Accept-Encoding"
        assert int(response.headers["content-length"]) == len(WASM)
        assert response.content == WASM

    def test_sends_plain_bytes_for_range_requests(self, client):
        """A byte range is taken from the uncompressed file."""
        response = client.get(
            "/main.dart.wasm", headers={**GZIP, "Range": "bytes=256-511"}
        )

        assert response.status_code == 206
        assert "content-encoding" not in response.headers
        assert response.content == WASM[256:512]

    def test_head_request_gets_compressed_headers(self, client):
        """A `HEAD` request gets the compressed file's headers and no body."""
        get = client.get("/main.dart.wasm", headers=GZIP)
        head = client.head("/main.dart.wasm", headers=GZIP)

        assert head.status_code == 200
        assert head.headers["content-encoding"] == "gzip"
        assert head.headers["content-length"] == get.headers["content-length"]
        assert head.headers["etag"] == get.headers["etag"]
        assert head.content == b""

    @pytest.mark.parametrize("path", ["/small.js", "/logo.png"])
    def test_sends_small_and_binary_files_as_is(self, client, path):
        """Files too small or already compressed are not compressed."""
        response = client.get(path, headers=GZIP)

        assert response.status_code == 200
        assert "content-encoding" not in response.headers
        assert "vary" not in response.headers

    def test_compresses_the_patched_index(self, web):
        """The index served for app routes is compressed when large enough."""
        (web / "index.html").write_text(f"<html><body>{'x' * 4096}</body></html>")
        app = FastAPI()
        app.mount("/", static_files.FletStaticFiles())
        with TestClient(app) as client:
            response = client.get("/some/route", headers=GZIP)

        assert response.status_code == 200
        assert response.headers["content-encoding"] == "gzip"
        assert "x" * 4096 in response.text


class TestCompressedCopies:
    def test_compresses_each_file_once(self, client, monkeypatch):
        """Later requests reuse the compressed copy."""
        calls = []
        write_gzip = static_files.write_gzip
        monkeypatch.setattr(
            static_files,
            "write_gzip",
            lambda *args: calls.append(args[0]) or write_gzip(*args),
        )

        for _ in range(3):
            assert client.get("/main.dart.wasm", headers=GZIP).content == WASM

        assert len(calls) == 1

    def test_compresses_a_changed_file_again(self, client, web):
        """A file changed while the server runs is served with its new content."""
        assert client.get("/main.dart.wasm", headers=GZIP).content == WASM

        changed = WASM[::-1]
        path = web / "main.dart.wasm"
        path.write_bytes(changed)
        stat = path.stat()
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns + 1_000_000_000))

        assert client.get("/main.dart.wasm", headers=GZIP).content == changed

    def test_paths_naming_the_same_file_share_one_copy(self, client, web, monkeypatch):
        """Differently cased paths to one file are compressed once."""
        if not (web / "MAIN.DART.WASM").exists():
            pytest.skip("The file system is case-sensitive")
        calls = []
        write_gzip = static_files.write_gzip
        monkeypatch.setattr(
            static_files,
            "write_gzip",
            lambda *args: calls.append(args[0]) or write_gzip(*args),
        )

        for path in ["/main.dart.wasm", "/MAIN.dart.wasm", "/Main.Dart.Wasm"]:
            assert client.get(path, headers=GZIP).content == WASM

        assert len(calls) == 1

    def test_compressed_copy_is_reproducible(self, web, tmp_path):
        """Compressing a file twice gives the same bytes and modification time."""
        source = web / "main.dart.wasm"
        stat = source.stat()
        first, second = tmp_path / "first.gz", tmp_path / "second.gz"
        static_files.write_gzip(str(source), str(first), stat)
        static_files.write_gzip(str(source), str(second), stat)

        assert first.read_bytes() == second.read_bytes()
        assert gzip.decompress(first.read_bytes()) == WASM
        assert first.stat().st_mtime_ns == stat.st_mtime_ns

    def test_unfinished_copy_is_removed(self, web, tmp_path, monkeypatch):
        """A copy that fails partway through writing leaves no file behind."""

        def fail(src, dst):
            dst.write(src.read(1024))
            raise OSError("No space left on device")

        monkeypatch.setattr(static_files.shutil, "copyfileobj", fail)
        source = web / "main.dart.wasm"
        target = tmp_path / "copies" / "main.gz"
        target.parent.mkdir()

        with pytest.raises(OSError):
            static_files.write_gzip(str(source), str(target), source.stat())

        assert list(target.parent.iterdir()) == []

    def test_sends_plain_file_when_compression_fails(self, client, monkeypatch):
        """A failure to write the compressed copy falls back to the plain file."""

        def fail(*args):
            raise OSError("No space left on device")

        monkeypatch.setattr(static_files, "write_gzip", fail)
        response = client.get("/main.dart.wasm", headers=GZIP)

        assert response.status_code == 200
        assert "content-encoding" not in response.headers
        assert response.content == WASM


class TestRevalidation:
    def test_compressed_and_plain_files_have_different_etags(self, client):
        """Caches can tell the two encodings of a file apart."""
        compressed = client.get("/main.dart.wasm", headers=GZIP)
        plain = client.get("/main.dart.wasm", headers={"Accept-Encoding": "identity"})

        assert compressed.headers["etag"] != plain.headers["etag"]
        assert compressed.headers["last-modified"] == plain.headers["last-modified"]

    def test_cached_compressed_file_is_not_modified(self, client):
        """The `ETag` of a cached compressed file gets `304 Not Modified`."""
        etag = client.get("/main.dart.wasm", headers=GZIP).headers["etag"]

        response = client.get(
            "/main.dart.wasm", headers={**GZIP, "If-None-Match": etag}
        )

        assert response.status_code == 304
        assert response.headers["vary"] == "Accept-Encoding"

    def test_compressed_etag_does_not_match_plain_file(self, client):
        """A plain request with the compressed file's `ETag` gets the file."""
        etag = client.get("/main.dart.wasm", headers=GZIP).headers["etag"]

        response = client.get(
            "/main.dart.wasm",
            headers={"Accept-Encoding": "identity", "If-None-Match": etag},
        )

        assert response.status_code == 200
        assert response.content == WASM

    def test_cached_compressed_file_is_revalidated_by_date(self, client):
        """`If-Modified-Since` alone gets a `304` for the compressed file."""
        compressed = client.get("/main.dart.wasm", headers=GZIP)

        response = client.get(
            "/main.dart.wasm",
            headers={
                **GZIP,
                "If-Modified-Since": compressed.headers["last-modified"],
            },
        )

        assert response.status_code == 304
        assert response.headers["etag"] == compressed.headers["etag"]

    def test_plain_etag_does_not_match_compressed_file(self, client):
        """A gzip request with the plain file's `ETag` gets the compressed file."""
        plain = client.get("/main.dart.wasm", headers={"Accept-Encoding": "identity"})

        response = client.get(
            "/main.dart.wasm",
            headers={
                **GZIP,
                "If-None-Match": plain.headers["etag"],
                "If-Modified-Since": plain.headers["last-modified"],
            },
        )

        assert response.status_code == 200
        assert response.headers["content-encoding"] == "gzip"
        assert response.content == WASM

    def test_etag_changes_with_the_file(self, client, web):
        """Changed content of the same modification time gets a new `ETag`."""
        path = web / "main.dart.wasm"
        path.write_bytes(b"A" * 1024)
        stat = path.stat()
        old = client.get("/main.dart.wasm", headers=GZIP)

        path.write_bytes(b"A" * 1025)
        os.utime(path, ns=(stat.st_atime_ns, stat.st_mtime_ns))
        response = client.get(
            "/main.dart.wasm", headers={**GZIP, "If-None-Match": old.headers["etag"]}
        )

        assert response.status_code == 200
        assert response.headers["etag"] != old.headers["etag"]
        assert response.content == b"A" * 1025
