import gzip
import hashlib
import logging
import mimetypes
import os
import shutil
import tempfile
from email.utils import parsedate
from pathlib import Path
from typing import Optional, Union

import anyio
import anyio.to_thread
from fastapi.staticfiles import StaticFiles
from starlette.datastructures import Headers
from starlette.responses import FileResponse, Response
from starlette.staticfiles import NotModifiedResponse
from starlette.types import Receive, Scope, Send

import flet_web.fastapi as flet_fastapi
from flet.controls.types import RouteUrlStrategy, WebRenderer
from flet.utils import Once, get_bool_env_var
from flet_web import (
    get_package_web_dir,
    patch_font_manifest_json,
    patch_index_html,
    patch_manifest_json,
)
from flet_web.fastapi.flet_app_manager import app_manager

logger = logging.getLogger(flet_fastapi.__name__)

# Ensure correct MIME types on platforms (e.g. Windows)
# that do not register them by default.
mimetypes.add_type("text/javascript", ".mjs")
mimetypes.add_type("application/wasm", ".wasm")

# Text and WebAssembly files shrink about 3x with gzip; images, archives and
# `.woff2` fonts are already compressed.
COMPRESSIBLE_EXTENSIONS = {
    ".css",
    ".html",
    ".js",
    ".json",
    ".map",
    ".mjs",
    ".otf",
    ".svg",
    ".ttf",
    ".txt",
    ".wasm",
    ".xml",
}

# Below this size, compression saves less than it costs.
MIN_COMPRESSED_FILE_SIZE = 1024


def resolve_assets_dir(assets_dir: Optional[str]) -> Optional[str]:
    """
    Resolve an app's assets directory to an existing absolute path.

    A relative path is resolved against the current working directory, which
    matches `ft.run(export_asgi_app=True)` - the other way a Flet app is served
    from a server process started externally (e.g. by `uvicorn`).

    Args:
        assets_dir: Path to the app's assets directory, absolute or relative.

    Returns:
        The resolved absolute path, or `None` if `assets_dir` was not set or
            does not exist.
    """

    if not assets_dir:
        return None

    path = Path(assets_dir)
    if not path.is_absolute():
        path = Path.cwd().joinpath(path)
    resolved = str(path.resolve())

    if not os.path.exists(resolved):
        logger.warning(f"assets_dir does not exist: {resolved}")
        return None

    return resolved


def is_compressible(path: str, stat_result: os.stat_result) -> bool:
    """
    Whether a static file is served gzip-compressed to browsers that accept it.

    Args:
        path: Path of the file.
        stat_result: The file's `os.stat()` result.
    """

    return (
        os.path.splitext(path)[1].lower() in COMPRESSIBLE_EXTENSIONS
        and stat_result.st_size >= MIN_COMPRESSED_FILE_SIZE
    )


def accepts_gzip(accept_encoding: str) -> bool:
    """
    Whether an `Accept-Encoding` request header allows a gzip response.

    Args:
        accept_encoding: Value of the header, e.g. `"gzip, deflate, br"`.

    Returns:
        `True` if `gzip`, or else `*`, is listed without `q=0`.
    """

    qualities = {}
    for coding in accept_encoding.split(","):
        name, *params = coding.split(";")
        quality = 1.0
        for param in params:
            key, _, value = param.partition("=")
            if key.strip().lower() == "q":
                try:
                    quality = float(value)
                except ValueError:
                    quality = 0.0
        qualities[name.strip().lower()] = quality
    return qualities.get("gzip", qualities.get("*", 0.0)) > 0


def write_gzip(source: str, target: str, stat_result: os.stat_result):
    """
    Write a gzip-compressed copy of a file.

    The copy gets the source's modification time, so that it is served with the
    same `Last-Modified` header. A copy left unfinished by an error is removed.

    Args:
        source: Path of the file to compress.
        target: Path of the compressed copy.
        stat_result: The source's `os.stat()` result.
    """

    temp = f"{target}.tmp"
    try:
        with (
            open(source, "rb") as src,
            open(temp, "wb") as raw,
            gzip.GzipFile(
                filename="", mode="wb", compresslevel=6, fileobj=raw, mtime=0
            ) as dst,
        ):
            shutil.copyfileobj(src, dst)
        os.utime(temp, ns=(stat_result.st_atime_ns, stat_result.st_mtime_ns))
        os.replace(temp, target)
    finally:
        if os.path.exists(temp):
            os.remove(temp)


class FletStaticFiles(StaticFiles):
    """
    Serve Flet app static files.

    Text and WebAssembly files, like the web client's `main.dart.wasm` and
    `main.dart.js`, are sent gzip-compressed to browsers that accept it, which
    makes them about 3x smaller to download. Each file is compressed once, in a
    worker thread, on its first request, and the compressed copy is kept in a
    temporary directory until the server exits. Byte range requests get the
    uncompressed file.

    Args:
        assets_dir: Path to app's assets directory. A relative path is resolved
            against the current working directory.
        app_name: PWA application name.
        app_short_name: PWA application short name.
        app_description: PWA application description.
        web_renderer: Type of web renderer, as a `WebRenderer` or its value, e.g.
            `"canvaskit"`.
        route_url_strategy: Routing URL strategy, as a `RouteUrlStrategy` or its
            value, e.g. `"hash"`.
        no_cdn: Whether not load CanvasKit, Pyodide, and fonts from CDN.
        websocket_endpoint_path: Path of Flet app WebSocket handler. A path
            without a leading `/` is resolved against the app mount path.
            Defaults to `ws`.
    """

    def __init__(
        self,
        proxy_path: Optional[str] = None,
        assets_dir: Optional[str] = None,
        app_name: Optional[str] = None,
        app_short_name: Optional[str] = None,
        app_description: Optional[str] = None,
        web_renderer: WebRenderer = WebRenderer.AUTO,
        route_url_strategy: RouteUrlStrategy = RouteUrlStrategy.PATH,
        no_cdn: bool = False,
        websocket_endpoint_path: Optional[str] = None,
    ) -> None:
        self.index = ["index.html"]
        self.manifest_json = ["manifest.json"]
        self.font_manifest_json = ["assets", "FontManifest.json"]
        self.__proxy_path = proxy_path
        self.__assets_dir = assets_dir
        self.__app_name = app_name
        self.__app_short_name = app_short_name
        self.__app_description = app_description
        self.__web_renderer = WebRenderer(web_renderer)
        self.__route_url_strategy = RouteUrlStrategy(route_url_strategy)
        self.__no_cdn = no_cdn
        self.__websocket_endpoint_path = websocket_endpoint_path
        self.__once = Once()
        self.__gzip_dir: Optional[str] = None
        self.__gzip_locks: dict[str, anyio.Lock] = {}
        self.__gzip_failures: set[str] = set()

        env_web_renderer = os.getenv("FLET_WEB_RENDERER")
        if env_web_renderer:
            self.__web_renderer = WebRenderer(env_web_renderer)

        env_route_url_strategy = os.getenv("FLET_WEB_ROUTE_URL_STRATEGY")
        if env_route_url_strategy:
            self.__route_url_strategy = RouteUrlStrategy(env_route_url_strategy)

        env_no_cdn = get_bool_env_var("FLET_WEB_NO_CDN")
        if env_no_cdn is not None:
            self.__no_cdn = env_no_cdn

        logger.info(f"Web renderer configured: {self.__web_renderer}")
        logger.info(f"Route URL strategy configured: {self.__route_url_strategy}")
        logger.info(f"No CDN configured: {self.__no_cdn}")

    @property
    def route_url_strategy(self) -> RouteUrlStrategy:
        """
        The route URL strategy written into the served `index.html`: the
        `route_url_strategy` argument, or `FLET_WEB_ROUTE_URL_STRATEGY` if set.
        """
        return self.__route_url_strategy

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.__once.do(self.__config, scope["root_path"])
        await super().__call__(scope, receive, send)

    def file_response(
        self,
        full_path: Union[str, os.PathLike[str]],
        stat_result: os.stat_result,
        scope: Scope,
        status_code: int = 200,
    ) -> Response:
        """
        Respond with a static file, adding `Vary: Accept-Encoding` to
        compressible ones.

        Unlike `StaticFiles`, this never responds with `304 Not Modified`:
        `get_response()` checks the browser's cached copy once it has picked
        the plain or compressed file.
        """
        response = FileResponse(
            full_path, status_code=status_code, stat_result=stat_result
        )
        if is_compressible(str(full_path), stat_result):
            # Tells caches that the response depends on the browser's
            # `Accept-Encoding`, so they keep the plain and gzip versions apart.
            response.headers["Vary"] = "Accept-Encoding"
        return response

    async def get_response(self, path: str, scope: Scope) -> Response:
        """
        Respond with a static file, gzip-compressed if the browser accepts it.

        Args:
            path: Requested path, relative to the mounted static root.
            scope: ASGI request scope.

        Returns:
            The compressed file for a `200` response of a compressible file to a
                request that accepts gzip and has no `Range` header; otherwise
                the response of `StaticFiles`. Either is `304 Not Modified` if
                the browser has that same file cached.
        """

        response = await super().get_response(path, scope)
        if response.status_code != 200 or not isinstance(response, FileResponse):
            return response

        request_headers = Headers(scope=scope)
        if (
            response.stat_result is not None
            and is_compressible(str(response.path), response.stat_result)
            and "range" not in request_headers
            and accepts_gzip(request_headers.get("accept-encoding", ""))
        ):
            # Derived from the plain file's `ETag`, so it changes whenever the
            # file does, and never equals it.
            etag = response.headers["etag"].removesuffix('"') + '-gzip"'
            gzip_headers = Headers(
                {
                    "etag": etag,
                    "last-modified": response.headers["last-modified"],
                    "vary": "Accept-Encoding",
                }
            )
            # Checked before compressing, so a browser revalidating its copy
            # after a server restart doesn't wait for the file to be compressed.
            if self.is_not_modified(gzip_headers, request_headers):
                return NotModifiedResponse(gzip_headers)

            compressed = await self.__compress(str(response.path), response.stat_result)
            if compressed:
                gzip_path, gzip_stat = compressed
                response = FileResponse(
                    gzip_path,
                    stat_result=gzip_stat,
                    media_type=response.media_type,
                    headers={
                        "Content-Encoding": "gzip",
                        "ETag": etag,
                        "Vary": "Accept-Encoding",
                    },
                )

        if self.is_not_modified(response.headers, request_headers):
            return NotModifiedResponse(response.headers)
        return response

    def is_not_modified(
        self, response_headers: Headers, request_headers: Headers
    ) -> bool:
        """
        Whether the browser's cached copy of a file is still current.

        `If-None-Match`, when sent, decides alone, so a cached copy in the
        other encoding, which has the same `Last-Modified`, is never taken as
        current.

        Args:
            response_headers: Headers of the response that would be sent.
            request_headers: Headers of the request.
        """

        if if_none_match := request_headers.get("if-none-match"):
            tags = [tag.strip().removeprefix("W/") for tag in if_none_match.split(",")]
            return response_headers["etag"] in tags or "*" in tags

        if_modified_since = parsedate(request_headers.get("if-modified-since", ""))
        last_modified = parsedate(response_headers.get("last-modified", ""))
        return (
            if_modified_since is not None
            and last_modified is not None
            and if_modified_since >= last_modified
        )

    async def __compress(
        self, path: str, stat_result: os.stat_result
    ) -> Optional[tuple[str, os.stat_result]]:
        """
        Get the gzip-compressed copy of a file, compressing it first if needed.

        Copies are keyed by the file's identity on disk, size and modification
        time: a file changed while the server runs is compressed again, and
        paths that name the same file, such as differently cased ones on a
        case-insensitive file system, share one copy. Concurrent requests for
        the same file wait for one compression. A file that fails to compress
        is logged and not tried again until it changes.

        Args:
            path: Path of the file.
            stat_result: The file's `os.stat()` result.

        Returns:
            The path and `os.stat()` result of the compressed copy, or `None` if
                the file could not be compressed.
        """

        assert self.__gzip_dir
        identity = (
            f"{stat_result.st_dev}:{stat_result.st_ino}"
            if stat_result.st_ino
            else os.path.normcase(os.path.realpath(path))
        )
        key = hashlib.sha256(
            f"{identity}\0{stat_result.st_size}\0{stat_result.st_mtime_ns}".encode()
        ).hexdigest()
        if key in self.__gzip_failures:
            return None
        gzip_path = os.path.join(self.__gzip_dir, f"{key}.gz")

        def compress() -> os.stat_result:
            if not os.path.exists(gzip_path):
                write_gzip(path, gzip_path, stat_result)
            return os.stat(gzip_path)

        lock = self.__gzip_locks.setdefault(key, anyio.Lock())
        async with lock:
            if key in self.__gzip_failures:
                return None
            try:
                return gzip_path, await anyio.to_thread.run_sync(compress)
            except OSError as e:
                logger.warning(f"Could not compress {path}: {e}")
                self.__gzip_failures.add(key)
                return None

    def lookup_path(self, path: str) -> tuple[str, Optional[os.stat_result]]:
        """Resolve a static file path, with SPA fallback for client-side routes.

        With the `path` route URL strategy, route-like paths (no extension, or
        `.html`) that don't match a file fall back to `index.html` so the
        Flutter client can handle routing. Asset-like paths (any other
        extension) resolve to a real `404`.

        With the `hash` strategy, routes live in the URL fragment and never
        reach the server, so there is no fallback: any path that doesn't match
        a file resolves to a real `404` (with a `404.html` from the assets
        directory as its body, if there is one), while the mount root still
        serves `index.html`.

        Args:
            path: Requested path, relative to the mounted static root
                (e.g. `"about"`, `"sample.json"`).

        Returns:
            A `(full_path, stat_result)` tuple. When `stat_result` is
                `None`, Starlette responds with `404`.
        """
        logger.debug(f"StaticFiles.lookup_path: {self.__app_mount_path} {path}")
        full_path, stat_result = super().lookup_path(path)

        if (
            stat_result is not None
            or self.__route_url_strategy == RouteUrlStrategy.HASH
        ):
            return full_path, stat_result

        # Not found: SPA fallback only for route-like paths.
        ext = os.path.splitext(path)[1].lower()
        if ext == "" or ext == ".html":
            return super().lookup_path(self.index[0])

        return full_path, stat_result

    async def __config(self, root_path: str):
        """
        Prepare a patched temporary web root and initialize static file serving.

        The method resolves app mount path, copies baseline web files
        (`index.html`, `manifest.json`, and optionally `FontManifest.json`)
        from either user assets or packaged web assets, applies runtime
        substitutions, and configures the underlying
        fastapi `StaticFiles` instance.

        Args:
            root_path: ASGI root path used to compute mounted base URL.
        """

        if self.__proxy_path:
            self.__app_mount_path = self.__proxy_path + root_path
        else:
            self.__app_mount_path = root_path

        # where modified index.html is stored
        temp_dir = tempfile.mkdtemp()
        app_manager.add_temp_dir(temp_dir)
        logger.info(f"Temp dir created for patched index and manifest: {temp_dir}")

        # where gzip-compressed copies of served files are stored; outside
        # temp_dir, which is served
        self.__gzip_dir = tempfile.mkdtemp()
        app_manager.add_temp_dir(self.__gzip_dir)

        # "standard" web files
        web_dir = get_package_web_dir()
        if os.getenv("FLET_WEB_PATH"):
            logger.info(f"Web root set via FLET_WEB_PATH: {web_dir}")
        else:
            logger.info(f"Web root: {web_dir}")

        if not os.path.exists(web_dir):
            raise RuntimeError(f"Web root path not found: {web_dir}")

        # user-defined assets
        self.__assets_dir = resolve_assets_dir(self.__assets_dir)

        logger.info(f"Assets dir: {self.__assets_dir}")

        def copy_temp_web_file(paths: list[str]):
            """
            Copy a web asset into the temporary patched web directory.

            Source precedence is user-provided assets directory first, then
            the packaged web directory.

            Args:
                paths: Path segments relative to the web root.
            """

            if self.__assets_dir and os.path.exists(
                p := os.path.join(self.__assets_dir, *paths)
            ):
                src_path = p
            else:
                src_path = os.path.join(web_dir, *paths)
            dst_path = os.path.join(temp_dir, *paths)
            Path(dst_path).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src_path, dst_path)

        # copy index.html from assets_dir or web_dir
        copy_temp_web_file(self.index)

        # copy manifest.json from assets_dir or web_dir
        copy_temp_web_file(self.manifest_json)

        # The WebSocket route is registered relative to the app mount path,
        # while the web client resolves `flet.webSocketEndpoint` against the
        # server root - so a relative endpoint name must be prefixed with the
        # mount path to produce a root-absolute path.
        ws_path = self.__websocket_endpoint_path or "ws"
        if not ws_path.startswith("/"):
            mount_path = self.__app_mount_path.strip("/")
            ws_path = f"{'' if mount_path == '' else '/' + mount_path}/{ws_path}"

        # replace variables in index.html and manifest.json
        patch_index_html(
            index_path=os.path.join(temp_dir, *self.index),
            base_href=self.__app_mount_path,
            websocket_endpoint_path=ws_path,
            app_name=self.__app_name,
            app_description=self.__app_description,
            web_renderer=self.__web_renderer,
            route_url_strategy=self.__route_url_strategy,
            no_cdn=self.__no_cdn,
        )

        patch_manifest_json(
            manifest_path=os.path.join(temp_dir, *self.manifest_json),
            app_name=self.__app_name,
            app_short_name=self.__app_short_name,
            app_description=self.__app_description,
        )

        if self.__no_cdn:
            # copy FontManifest.json from assets_dir or web_dir
            copy_temp_web_file(self.font_manifest_json)
            patch_font_manifest_json(
                manifest_path=os.path.join(temp_dir, *self.font_manifest_json)
            )

        # set html=True to resolve the index even when no
        # the base path is passed in
        super().__init__(directory=temp_dir, packages=None, html=True, check_dir=True)

        # add the rest of dirs
        if self.__assets_dir:
            self.all_directories.append(self.__assets_dir)

        self.all_directories.append(web_dir)
