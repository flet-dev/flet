import asyncio
import contextlib
from collections import deque
from dataclasses import dataclass, field
from typing import Callable, Optional

import flet as ft

__all__ = ["MatplotlibChartCanvas", "MatplotlibChartCanvasResizeEvent"]


@dataclass
class MatplotlibChartCanvasResizeEvent(ft.Event["MatplotlibChartCanvas"]):
    """
    Event emitted when the canvas reports a new rendered size.
    """

    width: float = field(metadata={"data_field": "w"})
    """New width of the canvas in logical pixels."""

    height: float = field(metadata={"data_field": "h"})
    """New height of the canvas in logical pixels."""


@ft.control("MatplotlibChartCanvas")
class MatplotlibChartCanvas(ft.LayoutControl):
    """
    Display widget for matplotlib WebAgg-style image streams.

    Receives either raw RGBA full frames (local transports) or full and
    incremental "diff" PNG frames (remote WebSocket) and displays them,
    holding at most one decoded image at a time. Frames flow over a
    dedicated [ft.DataChannel] rather than the regular Flet protocol, so
    the frame bytes skip MsgPack encode/decode and travel at
    memory-bandwidth-class speed in embedded native mode (per-channel
    PythonBridge) and at near-bandwidth speed in web/dev modes (raw-byte
    frames muxed over the protocol transport).

    Wire format on the data channel (one byte of opcode followed by the
    payload):

    | opcode | payload                       | meaning                                 |
    |--------|-------------------------------|-----------------------------------------|
    | 0x01   | PNG bytes                     | apply_full — replace backdrop           |
    | 0x02   | PNG bytes                     | apply_diff — composite onto backbuffer  |
    | 0x03   | (empty)                       | clear — drop backdrop + backbuffer      |
    | 0x04   | [w u32 LE][h u32 LE][RGBA]    | raw full frame, premultiplied RGBA8888  |

    The reverse-direction `resize` event (Dart → Python, small JSON-shaped
    payload) stays on the existing Flet protocol channel — no reason to
    move tiny control events off it.
    """

    resize_interval: ft.Number = 10
    """
    Sampling interval in milliseconds for `on_resize` event.
    """

    on_resize: Optional[ft.EventHandler[MatplotlibChartCanvasResizeEvent]] = None
    """
    Called when the size of this canvas has changed.
    """

    on_data_channel_open: Optional[ft.EventHandler[ft.DataChannelOpenEvent]] = None
    """
    Framework hook — Dart fires this when it opens the data channel during
    `initState`. The default handler captures the channel for use by
    apply_full / apply_diff / clear. Override only if you need to do
    something extra at attach-time.
    """

    def init(self) -> None:
        # `init` is the @ft.control post-construct lifecycle hook (runs
        # before `did_mount`). Wire up the default channel-capture handler.
        self._channel: Optional[ft.DataChannel] = None
        # FIFO of per-frame ack futures. Each `apply_*` enqueues a future
        # and `awaits` it; `_on_dart_message` pops the head and resolves
        # it when Dart's `[0xFF]` ack arrives. The await is what makes
        # producer-side callers (e.g. MatplotlibChart._receive_loop)
        # block — events queued during the wait are processed *after*
        # the ack instead of being dropped by stale gate checks.
        self._pending_acks: deque[asyncio.Future] = deque()
        # Optional plain callback for observers that want to be notified
        # on every frame ack (e.g. perf instrumentation). Fires alongside
        # the future resolution; not load-bearing for backpressure.
        self._on_frame_applied: Optional[Callable[[], None]] = None
        if self.on_data_channel_open is None:
            self.on_data_channel_open = self._capture_channel

    def _capture_channel(self, e: ft.DataChannelOpenEvent) -> None:
        # Single-channel widget; no need to dispatch on e.channel_name.
        self._channel = self.get_data_channel(e.channel_id)
        self._channel.on_bytes(self._on_dart_message)

    def _on_dart_message(self, payload: bytes) -> None:
        # Wire format on the reverse direction (Dart → Python):
        #   [0xFF] — frame_applied ack. Sent by Dart after each apply_full /
        #            apply_diff / clear completes on its end. Restores the
        #            round-trip backpressure that `_invoke_method` used to
        #            provide implicitly in 0.85.
        if not payload or payload[0] != 0xFF:
            return
        # Resolve the head future so the matching `apply_*` await returns.
        if self._pending_acks:
            fut = self._pending_acks.popleft()
            if not fut.done():
                fut.set_result(None)
        # Then fire the observer callback (if any).
        cb = self._on_frame_applied
        if cb is not None:
            with contextlib.suppress(Exception):
                cb()

    def set_on_frame_applied(self, cb: Optional[Callable[[], None]]) -> None:
        """Register a side-channel callback invoked on every frame ack.

        Useful for instrumentation. Backpressure is handled by awaiting
        the result of `apply_full` / `apply_diff` / `clear` directly —
        this callback is a fire-and-forget observer, not part of the
        gating path.
        """
        self._on_frame_applied = cb

    async def _send_and_wait(self, packet: bytes) -> None:
        """Send a channel packet and await Dart's ack.

        Awaiting blocks the caller until `[0xFF]` arrives on the channel,
        re-creating the 0.85 `_invoke_method` round-trip semantics:
        events that arrive in the producer's queue during the wait stay
        queued (instead of being processed eagerly against a stale
        `_waiting` flag).
        """
        if self._channel is None:
            return
        loop = asyncio.get_running_loop()
        fut: asyncio.Future = loop.create_future()
        self._pending_acks.append(fut)
        self._channel.send(packet)
        await fut

    async def apply_full(self, image_bytes: bytes) -> None:
        """
        Replace the current displayed image with a full PNG frame.

        Args:
            image_bytes: PNG bytes of the complete frame.
        """
        await self._send_and_wait(b"\x01" + image_bytes)

    async def apply_diff(self, image_bytes: bytes) -> None:
        """
        Composite an incremental "diff" PNG frame onto the current image.

        Pixels with non-zero alpha replace the corresponding pixels in the
        existing backbuffer; transparent pixels leave the backbuffer
        unchanged. If no backbuffer exists yet, the diff is treated as a
        full frame.

        Args:
            image_bytes: PNG bytes of the diff frame.
        """
        await self._send_and_wait(b"\x02" + image_bytes)

    async def clear(self) -> None:
        """
        Clear the displayed image and discard the backbuffer.
        """
        await self._send_and_wait(b"\x03")

    @staticmethod
    def encode_raw_frame(width: int, height: int, rgba) -> bytes:
        """
        Encode a raw full frame into a 0x04 wire packet.

        Args:
            width: Frame width in physical pixels.
            height: Frame height in physical pixels.
            rgba: Premultiplied RGBA8888 pixels, `width * height * 4` bytes
                (bytes-like; a memoryview aliasing a live buffer is copied
                here exactly once).
        """
        pkt = bytearray(9 + len(rgba))
        pkt[0] = 0x04
        pkt[1:5] = width.to_bytes(4, "little")
        pkt[5:9] = height.to_bytes(4, "little")
        pkt[9:] = rgba
        return bytes(pkt)

    async def apply_raw(self, width: int, height: int, rgba: bytes) -> None:
        """
        Replace the displayed image with a raw premultiplied-RGBA full frame.

        Args:
            width: Frame width in physical pixels.
            height: Frame height in physical pixels.
            rgba: Premultiplied RGBA8888 pixels, `width * height * 4` bytes.
        """
        await self._send_and_wait(self.encode_raw_frame(width, height, rgba))

    async def apply_raw_packet(self, packet: bytes) -> None:
        """
        Send a pre-encoded 0x04 raw-frame packet (avoids a second copy).

        Args:
            packet: Complete wire packet produced by `encode_raw_frame`.
        """
        await self._send_and_wait(packet)
