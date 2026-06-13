import contextlib
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

    Receives full and incremental "diff" PNG frames and composites them in
    CPU memory, holding at most one decoded image for display at a time.
    Frames flow over a dedicated [ft.DataChannel] rather than the regular
    Flet protocol, so the PNG bytes skip MsgPack encode/decode and travel
    at memory-bandwidth-class speed in embedded native mode (per-channel
    PythonBridge) and at near-bandwidth speed in web/dev modes (raw-byte
    frames muxed over the protocol transport).

    Wire format on the data channel (one byte of opcode followed by the
    PNG payload):

    | opcode | payload    | meaning                                    |
    |--------|------------|--------------------------------------------|
    | 0x01   | PNG bytes  | apply_full — replace backdrop              |
    | 0x02   | PNG bytes  | apply_diff — composite onto backbuffer     |
    | 0x03   | (empty)    | clear — drop backdrop + backbuffer         |

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
        # Backpressure ack callback — invoked when Dart finishes applying
        # a frame on its end. Producer-side widgets (e.g. MatplotlibChart)
        # set this to gate the next frame so the Dart-side queue stays
        # bounded under interactive load.
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
        #            provide implicitly.
        if not payload:
            return
        if payload[0] == 0xFF:
            cb = self._on_frame_applied
            if cb is not None:
                with contextlib.suppress(Exception):
                    cb()

    def set_on_frame_applied(self, cb: Optional[Callable[[], None]]) -> None:
        """Register a callback invoked when Dart finishes applying a frame.

        Producer widgets use this to gate frame emission — e.g. matplotlib
        clears its `_waiting` flag here so the next `draw` message from
        the figure is honored. Without this gate, the producer would push
        frames into the Dart-side queue faster than they're rendered,
        causing the UI to hog and then replay buffered frames in a burst.
        """
        self._on_frame_applied = cb

    def apply_full(self, image_bytes: bytes) -> None:
        """
        Replace the current displayed image with a full PNG frame.

        Args:
            image_bytes: PNG bytes of the complete frame.
        """
        if self._channel is None:
            return
        self._channel.send(b"\x01" + image_bytes)

    def apply_diff(self, image_bytes: bytes) -> None:
        """
        Composite an incremental "diff" PNG frame onto the current image.

        Pixels with non-zero alpha replace the corresponding pixels in the
        existing backbuffer; transparent pixels leave the backbuffer
        unchanged. If no backbuffer exists yet, the diff is treated as a
        full frame.

        Args:
            image_bytes: PNG bytes of the diff frame.
        """
        if self._channel is None:
            return
        self._channel.send(b"\x02" + image_bytes)

    def clear(self) -> None:
        """
        Clear the displayed image and discard the backbuffer.
        """
        if self._channel is None:
            return
        self._channel.send(b"\x03")
