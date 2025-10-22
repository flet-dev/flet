import asyncio
import base64
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
    TCP-based tester implementation that talks directly to
    the Flutter integration test harness.
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
        Starts the TCP server accepting connections from Flutter.

        Args:
            host: Host interface to bind to. Defaults to ``127.0.0.1``.
            port: Optional port to bind to. A random free port is used when
                not specified.

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
        buffer = bytearray()
        max_line_length = 16 * 1024 * 1024
        while True:
            chunk = await self._reader.read(4096)
            if not chunk:
                if buffer:
                    message = json.loads(buffer.decode("utf-8"))
                    self._dispatch_message(message)
                break
            buffer.extend(chunk)
            while True:
                newline_index = buffer.find(b"\n")
                if newline_index == -1:
                    if len(buffer) > max_line_length:
                        raise ValueError("Incoming message exceeds allowed size.")
                    break
                line = buffer[:newline_index]
                del buffer[: newline_index + 1]
                message = json.loads(line.decode("utf-8"))
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
        """
        Stops the TCP server and releases any bound resources.
        """
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None

    async def _ensure_connected(self):
        await self._connected.wait()
        if self._writer is None:
            raise ConnectionError("Remote tester is not connected.")

    async def _invoke(self, method: str, params: Optional[dict[str, Any]] = None):
        await self._ensure_connected()
        self._request_id += 1
        request_id = self._request_id

        loop = asyncio.get_running_loop()
        future: asyncio.Future[Any] = loop.create_future()
        self._pending[request_id] = future

        payload = {"id": request_id, "method": method}
        if params:
            payload["params"] = params

        async with self._send_lock:
            assert self._writer is not None
            self._writer.write(json.dumps(payload).encode("utf-8") + b"\n")
            await self._writer.drain()

        return await future

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
        await self._invoke("tap", {"id": finder.id})

    async def long_press(self, finder: Finder):
        await self._invoke("long_press", {"id": finder.id})

    async def enter_text(self, finder: Finder, text: str):
        await self._invoke("enter_text", {"id": finder.id, "text": text})

    async def mouse_hover(self, finder: Finder):
        await self._invoke("mouse_hover", {"id": finder.id})

    async def teardown(self):
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


def _with_optional(key: str, value: Any) -> dict[str, Any]:
    return {key: value} if value is not None else {}


def _serialize_duration(duration: Optional[DurationValue]) -> Any:
    if duration is None:
        return None
    if is_dataclass(duration):
        return asdict(duration)
    if isinstance(duration, (int, float)):
        return int(duration)
    return duration


def _serialize_key(value: KeyValue) -> Any:
    if value is None:
        return None
    if is_dataclass(value):
        return asdict(value)
    return value


def _serialize_icon(icon: IconData) -> Any:
    if icon is None:
        return None
    if hasattr(icon, "value"):
        return int(icon)
    return icon
