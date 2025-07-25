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

    Setting to `0` calls [`on_resize`][flet.canvas.Canvas.on_resize] immediately on every change.
    """

    on_resize: Optional[EventHandler[CanvasResizeEvent]] = None
    """
    Called when the size of this canvas has changed.
    """
