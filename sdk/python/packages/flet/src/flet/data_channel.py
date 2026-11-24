"""Widget-facing byte-channel API.

A `DataChannel` is a dedicated bidirectional byte transport between a
single widget's Dart side and its Python counterpart, separate from the
Flet control protocol. Used for bulk binary data — image frames, audio
buffers, ML tensors — that would otherwise pay MsgPack encode/decode
overhead through the regular protocol channel.

The transport implementation is chosen by the active Connection subclass:

- `FletDartBridgeServer` (embedded native via `dart_bridge`): each
  channel rides its own dedicated PythonBridge native port (4–7 GiB/s on
  M2 Pro).
- `FletSocketServer` / `flet_web.fastapi.FletApp` (dev mode, web with
  Python server): bytes are muxed over the active Flet protocol
  transport with a 1-byte type discriminator (0x01) + 4-byte channel id.

Allocation lives on the Dart side. The widget's Dart code calls
`FletBackend.of(context).openDataChannel()` in `initState`, then fires a
`data_channel_open` control event carrying `{channel_name, channel_id}`.
The Python widget declares `on_data_channel_open:
Optional[ft.EventHandler[DataChannelOpenEvent]] = None` and inside the
handler calls `self.get_data_channel(e.channel_id)` to attach.
"""

from __future__ import annotations

import contextlib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

from flet.controls.control_event import Event

if TYPE_CHECKING:
    from flet.messaging.connection import Connection


@dataclass
class DataChannelOpenEvent(Event["BaseControl"]):
    """Fired by Dart when it opens a DataChannel for a control. Carry the
    channel id (Dart native port in embedded mode, monotonic u32 in muxed
    fallback) plus a user-defined `channel_name` so widgets that open
    several channels can dispatch.

    Note: the field is `channel_name`, not `name`, because `Event.name`
    already carries the event's own name (`"data_channel_open"`).
    """

    channel_name: str = ""
    channel_id: int = 0


class DataChannel(ABC):
    """Abstract widget-facing byte channel."""

    @abstractmethod
    def on_bytes(self, handler: Callable[[bytes], None] | None) -> None:
        """Register a handler for bytes pushed from Dart. Pass `None` to
        clear. The handler runs synchronously on whatever thread the
        transport delivers from — push heavy work to a queue/worker."""
        ...

    @abstractmethod
    def send(self, payload: bytes) -> None:
        """Send bytes Python → Dart. Fire-and-forget."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Release the channel. Idempotent."""
        ...


class _DartBridgeDataChannel(DataChannel):
    """Embedded native mode: bytes flow over a dedicated PythonBridge port.
    `channel_id` is the Dart native port number minted on the Dart side.
    """

    def __init__(self, port: int) -> None:
        import dart_bridge  # type: ignore — built-in module from libdart_bridge

        self._port = port
        self._dart_bridge = dart_bridge
        self._handler: Callable[[bytes], None] | None = None
        self._closed = False

    def on_bytes(self, handler: Callable[[bytes], None] | None) -> None:
        self._handler = handler
        self._dart_bridge.set_enqueue_handler_func(self._port, handler)

    def send(self, payload: bytes) -> None:
        if self._closed:
            return
        self._dart_bridge.send_bytes(self._port, payload)

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        if self._handler is not None:
            with contextlib.suppress(Exception):
                self._dart_bridge.set_enqueue_handler_func(self._port, None)
            self._handler = None


class _ProtocolMuxedDataChannel(DataChannel):
    """Non-embedded modes: bytes ride the Flet protocol transport as
    `[0x01][channel_id:u32 LE][payload]` frames. The owning Connection
    routes inbound frames here via `_deliver()`.
    """

    def __init__(self, channel_id: int, conn: Connection) -> None:
        self._id = channel_id
        self._conn = conn
        self._handler: Callable[[bytes], None] | None = None
        self._closed = False

    def on_bytes(self, handler: Callable[[bytes], None] | None) -> None:
        self._handler = handler

    def send(self, payload: bytes) -> None:
        if self._closed:
            return
        # Connection knows the wire format for its transport (length
        # prefix on stream transports, none on message transports).
        self._conn.send_data_channel_frame(self._id, payload)

    def _deliver(self, payload: bytes) -> None:
        if self._closed:
            return
        handler = self._handler
        if handler is not None:
            try:
                handler(payload)
            except Exception:
                import logging

                logging.getLogger("flet").exception(
                    "DataChannel handler raised; channel id=%s", self._id
                )

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        # Connection's unregister is best-effort — duplicate unregisters
        # are safe.
        unreg = getattr(self._conn, "unregister_data_channel", None)
        if unreg is not None:
            with contextlib.suppress(Exception):
                unreg(self._id)
        self._handler = None
