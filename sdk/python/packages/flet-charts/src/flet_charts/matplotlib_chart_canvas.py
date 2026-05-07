from dataclasses import dataclass, field
from typing import Optional

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
    Avoids the per-frame `Picture.toImage` allocations that the generic
    `flet.canvas.Canvas` capture path uses, which on Flutter web
    (CanvasKit/WASM) accumulate and aren't promptly reclaimed by the JS GC
    during animation, causing browser memory growth.
    """

    resize_interval: ft.Number = 10
    """
    Sampling interval in milliseconds for `on_resize` event.
    """

    on_resize: Optional[ft.EventHandler[MatplotlibChartCanvasResizeEvent]] = None
    """
    Called when the size of this canvas has changed.
    """

    async def apply_full(self, image_bytes: bytes) -> None:
        """
        Replace the current displayed image with a full PNG frame.

        Args:
            image_bytes: PNG bytes of the complete frame.
        """
        await self._invoke_method("apply_full", arguments={"bytes": image_bytes})

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
        await self._invoke_method("apply_diff", arguments={"bytes": image_bytes})

    async def clear(self) -> None:
        """
        Clear the displayed image and discard the backbuffer.
        """
        await self._invoke_method("clear")
