from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number


@control("Rect")
class Rect(Shape):
    """
    Draws a rectangle.
    """

    x: Optional[Number] = None
    """
    The x-axis coordinate of the rectangle's top left point.
    """

    y: Optional[Number] = None
    """
    The y-axis coordinate of the rectangle's top left point.
    """

    width: Optional[Number] = None
    """
    Width of the rectangle.
    """

    height: Optional[Number] = None
    """
    Height of the rectangle.
    """

    border_radius: Optional[BorderRadiusValue] = None
    """
    Border radius of the rectangle.

    Type: [`BorderRadius`][flet.BorderRadius]
    """

    paint: Optional[Paint] = None
    """
    A style to draw a rectangle with. The value of this property is the instance of
    [`Paint`][flet.Paint] class.
    """
