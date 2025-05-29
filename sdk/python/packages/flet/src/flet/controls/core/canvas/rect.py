from typing import Optional

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Rect")
class Rect(Shape):
    """
    Draws a rectangle.
    """

    x: OptionalNumber = None
    """
    The x-axis coordinate of the rectangle's top left point.
    """

    y: OptionalNumber = None
    """
    The y-axis coordinate of the rectangle's top left point.
    """

    width: OptionalNumber = None
    """
    Width of the rectangle.
    """

    height: OptionalNumber = None
    """
    Height of the rectangle.
    """

    border_radius: OptionalBorderRadiusValue = None
    """
    Border radius of the rectangle.

    Value is of type [`BorderRadius`](https://flet.dev/docs/reference/types/borderradius).
    """

    paint: Optional[Paint] = None
    """
    A style to draw a rectangle with. The value of this property is the instance of
    [`Paint`](https://flet.dev/docs/reference/types/paint) class.
    """

