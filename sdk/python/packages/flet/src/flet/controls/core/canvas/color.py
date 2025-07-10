from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import BlendMode, ColorValue


@control("Color")
class Color(Shape):
    """
    Paints the given `color` onto the canvas, applying the given `blend_mode`, with
    the given color being the source and the background being the destination.
    """

    color: Optional[ColorValue] = None
    """
    Color to paint onto the canvas.
    """

    blend_mode: Optional[BlendMode] = None
    """
    Blend mode to apply.
    """
