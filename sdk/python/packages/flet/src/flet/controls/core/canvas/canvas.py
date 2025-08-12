from dataclasses import dataclass, field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import Event, EventHandler
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import Number

__all__ = ["Canvas", "CanvasResizeEvent"]


@dataclass
class CanvasResizeEvent(Event["Canvas"]):
    width: float = field(metadata={"data_field": "w"})
    """
    New width of the canvas.
    """

    height: float = field(metadata={"data_field": "h"})
    """
    New height of the canvas.
    """


@control("Canvas")
class Canvas(ConstrainedControl):
    """
    Canvas is a control for drawing arbitrary graphics using a set of primitives or
    "shapes" such as line, arc, path and text.
    """

    shapes: list[Shape] = field(default_factory=list)
    """
    A list of shapes to draw on this canvas.
    """

    content: Optional[Control] = None
    """
    The content of this canvas.
    """

    resize_interval: Number = 10
    """
    Sampling interval in milliseconds for `on_resize` event.

    Setting to `0` calls [`on_resize`][flet.canvas.Canvas.on_resize] immediately
    on every change.
    """

    on_resize: Optional[EventHandler[CanvasResizeEvent]] = None
    """
    Called when the size of this canvas has changed.
    """

    def before_update(self):
        super().before_update()
        if self.expand:
            if self.width is None:
                self.width = float("inf")
            if self.height is None:
                self.height = float("inf")

    async def capture(self, pixel_ratio: Optional[Number] = None):
        """
        Captures the current visual state of the canvas.

        The captured image is stored internally and will be rendered as a background
        beneath all subsequently drawn shapes.

        Args:
            pixel_ratio:
                The pixel density multiplier to use when rendering the capture.
                `1.0` means 1 device pixel per logical pixel (no scaling).
                Values greater than `1.0` produce higher-resolution captures.
                If `None`, the device's default pixel ratio is used.
        """
        await self._invoke_method("capture", arguments={"pixel_ratio": pixel_ratio})

    async def get_capture(self) -> bytes:
        """
        Retrieves the most recent canvas capture as PNG bytes.

        Returns:
            bytes: The captured image in PNG format, or an empty result
            if no capture has been made.
        """
        return await self._invoke_method("get_capture")

    async def clear_capture(self):
        """
        Clears the previously captured canvas image.

        After clearing, no background will be rendered from a prior capture.
        """
        await self._invoke_method("clear_capture")
