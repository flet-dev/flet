from flet.controls.base_control import control
from flet.controls.colors import Colors
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import BlendMode, ColorValue

__all__ = ["Color"]


@control("Color")
class Color(Shape):
    """
    Paints the given `color` onto the canvas, applying the given `blend_mode`, with
    the given color being the source and the background being the destination.
    """

    color: ColorValue = Colors.BLACK
    """
    Color to paint onto the canvas.
    """

    blend_mode: BlendMode = BlendMode.SRC_OVER
    """
    Blend mode to apply.
    """
