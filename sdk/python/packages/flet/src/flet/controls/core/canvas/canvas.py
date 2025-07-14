import asyncio
from dataclasses import dataclass, field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import Event, OptionalEventHandler
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import OptionalNumber


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
    The list of `Shape` objects (see below) to draw on the canvas.
    """

    content: Optional[Control] = None
    """
    TBD
    """

    resize_interval: OptionalNumber = None
    """
    Sampling interval in milliseconds for `on_resize` event.

    Defaults to `0` - call `on_resize` immediately on every change.
    """

    on_resize: OptionalEventHandler[CanvasResizeEvent] = None
    """
    Fires when the size of canvas has changed.

    Event object `e` is an instance of
    [CanvasResizeEvent](https://flet.dev/docs/reference/types/canvasresizeevent).
    """

    def before_update(self):
        super().before_update()
        if self.expand:
            if self.width is None:
                self.width = float("inf")
            if self.height is None:
                self.height = float("inf")

    async def capture_async(self):
        await self._invoke_method_async("capture")

    def capture(self):
        asyncio.create_task(self.capture_async())

    async def get_capture_async(self):
        return await self._invoke_method_async("get_capture")

    async def clear_capture_async(self):
        await self._invoke_method_async("capture")

    def clear_capture(self):
        asyncio.create_task(self.clear_capture_async())
