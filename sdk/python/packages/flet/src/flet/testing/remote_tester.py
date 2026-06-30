import asyncio
import base64
import contextlib
import json
from dataclasses import asdict, is_dataclass
from typing import Any, Optional

from flet.controls.duration import DurationValue
from flet.controls.keys import KeyValue
from flet.controls.types import IconData
from flet.testing.finder import Finder

__all__ = ["RemoteTester", "RemoteTesterError"]


class RemoteTesterError(RuntimeError):
    """Error returned from a remote tester invocation."""

    def __init__(self, message: str, stack: Optional[str] = None):
        super().__init__(message)
        self.stack = stack


class RemoteTester:
    """
    TCP server that drives the Flutter integration-test ``WidgetTester`` over an
    independent line-delimited JSON protocol (separate from Flet's own
    transport). The on-device app's ``RemoteWidgetTester`` connects to this
    server and executes the commands.
    """

    def __init__(self):
        self._server: Optional[asyncio.AbstractServer] = None
        self._reader: Optional[asyncio.StreamReader] = None
        self._writer: Optional[asyncio.StreamWriter] = None
        self._connected = asyncio.Event()
        self._closed = asyncio.Event()
        self._closed.set()
        self._pending: dict[int, asyncio.Future[Any]] = {}
        self._request_id = 0
        self._reader_task: Optional[asyncio.Task[Any]] = None
        self._send_lock = asyncio.Lock()
        self.host = "127.0.0.1"
        self.port: Optional[int] = None

    async def start(self, host: str = "127.0.0.1", port: Optional[int] = None) -> int:
        """
        Starts the TCP server accepting a connection from the Flutter app.

        Returns:
            Bound TCP port.
        """
        if self._server is not None:
            raise RuntimeError("RemoteTester server is already running.")

        self.host = host
        self._server = await asyncio.start_server(self._handle_client, host, port)
        sock = self._server.sockets[0]
        self.port = sock.getsockname()[1]
        return self.port

    async def _handle_client(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter
    ):
        if self._reader is not None:
            writer.close()
            await writer.wait_closed()
            return

        self._reader = reader
        self._writer = writer
        self._closed.clear()
        self._connected.set()
        self._reader_task = asyncio.create_task(self._read_loop())

        try:
            await self._reader_task
        finally:
            self._cleanup_connection()

    async def _read_loop(self):
        assert self._reader is not None
        reader = self._reader
        max_frame_length = 64 * 1024 * 1024
        while True:
            try:
                header = await reader.readexactly(4)
            except asyncio.IncompleteReadError:
                break
            length = int.from_bytes(header, "big")
            if length > max_frame_length:
                raise ValueError("Incoming frame exceeds allowed size.")
            try:
                payload = await reader.readexactly(length)
            except asyncio.IncompleteReadError:
                break
            message = json.loads(payload.decode("utf-8"))
            self._dispatch_message(message)

    def _dispatch_message(self, message: Any):
        request_id = message.get("id")
        future = self._pending.pop(request_id, None)
        if future is None:
            return
        if "error" in message:
            future.set_exception(
                RemoteTesterError(message["error"], message.get("stack"))
            )
        else:
            future.set_result(message.get("result"))

    def _cleanup_connection(self):
        for future in self._pending.values():
            if not future.done():
                future.set_exception(
                    ConnectionError("Remote tester connection was closed.")
                )
        self._pending.clear()
        self._reader = None
        self._writer = None
        self._reader_task = None
        self._connected.clear()
        self._closed.set()

    async def stop(self):
        """Stops the TCP server and releases any bound resources."""
        # Tear down the active client connection first. `_read_loop` blocks on
        # `readexactly` until it sees EOF, and the on-device app's socket close
        # does not always deliver that to us (observed on Linux), so without this
        # `Server.wait_closed()` below would hang forever waiting for the still
        # running `_handle_client`. Cancelling the read task lets `_handle_client`
        # finish; the timeout is a final safety net.
        if self._reader_task is not None and not self._reader_task.done():
            self._reader_task.cancel()
        if self._writer is not None:
            with contextlib.suppress(Exception):
                self._writer.close()
        if self._server is not None:
            self._server.close()
            with contextlib.suppress(asyncio.TimeoutError):
                await asyncio.wait_for(self._server.wait_closed(), timeout=5)
            self._server = None

    async def _ensure_connected(self):
        await self._connected.wait()
        if self._writer is None:
            raise ConnectionError("Remote tester is not connected.")

    async def _invoke(
        self,
        method: str,
        params: Optional[dict[str, Any]] = None,
        timeout: Optional[float] = 60,
    ):
        await self._ensure_connected()
        self._request_id += 1
        request_id = self._request_id

        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()
        self._pending[request_id] = future

        payload: dict[str, Any] = {"id": request_id, "method": method}
        if params:
            payload["params"] = params

        async with self._send_lock:
            assert self._writer is not None
            data = json.dumps(payload).encode("utf-8")
            self._writer.write(len(data).to_bytes(4, "big") + data)
            await self._writer.drain()

        try:
            if timeout is not None:
                return await asyncio.wait_for(future, timeout=timeout)
            return await future
        except asyncio.TimeoutError:
            self._pending.pop(request_id, None)
            raise TimeoutError(
                f"Timeout waiting for remote tester method {method}({params})"
            ) from None

    async def pump(self, duration: Optional[DurationValue] = None):
        await self._invoke(
            "pump", _with_optional("duration", _serialize_duration(duration))
        )

    async def pump_and_settle(self, duration: Optional[DurationValue] = None):
        await self._invoke(
            "pump_and_settle",
            _with_optional("duration", _serialize_duration(duration)),
        )

    async def find_by_text(self, text: str) -> Finder:
        finder = await self._invoke("find_by_text", {"text": text})
        return Finder(**finder)

    async def find_by_text_containing(self, pattern: str) -> Finder:
        finder = await self._invoke("find_by_text_containing", {"pattern": pattern})
        return Finder(**finder)

    async def find_by_key(self, key: KeyValue) -> Finder:
        finder = await self._invoke("find_by_key", {"key": _serialize_key(key)})
        return Finder(**finder)

    async def find_by_tooltip(self, value: str) -> Finder:
        finder = await self._invoke("find_by_tooltip", {"value": value})
        return Finder(**finder)

    async def find_by_icon(self, icon: IconData) -> Finder:
        finder = await self._invoke("find_by_icon", {"icon": _serialize_icon(icon)})
        return Finder(**finder)

    async def take_screenshot(self, name: str) -> bytes:
        data = await self._invoke("take_screenshot", {"name": name})
        return base64.b64decode(data)

    async def tap(self, finder: Finder):
        await self._invoke("tap", _finder_params(finder))

    async def long_press(self, finder: Finder):
        await self._invoke("long_press", _finder_params(finder))

    async def enter_text(self, finder: Finder, text: str):
        await self._invoke("enter_text", {**_finder_params(finder), "text": text})

    async def mouse_hover(self, finder: Finder):
        await self._invoke("mouse_hover", _finder_params(finder))

    async def teardown(self, timeout: Optional[float] = None):
        if not self.is_connected():
            return
        try:
            await self._invoke("teardown")
        finally:
            await self.wait_closed()

    async def wait_closed(self):
        await self._closed.wait()

    def is_connected(self) -> bool:
        return self._connected.is_set()

    async def wait_for_connection(self, timeout: Optional[float] = None):
        if timeout is not None:
            await asyncio.wait_for(self._connected.wait(), timeout)
        else:
            await self._connected.wait()


def _finder_params(finder: Finder) -> dict[str, Any]:
    return {"finder_id": finder.id, "finder_index": finder.index}


def _with_optional(key: str, value: Any) -> dict[str, Any]:
    return {key: value} if value is not None else {}


def _serialize_duration(duration: Optional[DurationValue]) -> Any:
    if duration is None:
        return None
    if is_dataclass(duration) and not isinstance(duration, type):
        return asdict(duration)
    if isinstance(duration, (int, float)):
        return int(duration)
    return duration


def _serialize_key(value: KeyValue) -> Any:
    if value is None:
        return None
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    return value


def _serialize_icon(icon: IconData) -> Any:
    if icon is None:
        return None
    if hasattr(icon, "value"):
        return int(icon)
    return icon
