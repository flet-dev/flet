from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import BlendMode, OptionalColorValue


@control("Color")
class Color(Shape):
    """
    Paints the given `color` onto the canvas, applying the given `blend_mode`, with
    the given color being the source and the background being the destination.
    """

    color: OptionalColorValue = None
    """
    [Color](https://flet.dev/docs/reference/colors) to paint onto the canvas.
    """

    blend_mode: Optional[BlendMode] = None
    """
    Blend mode to apply.

    Value is of type [`BlendMode`](https://flet.dev/docs/reference/types/blendmode).
    """

