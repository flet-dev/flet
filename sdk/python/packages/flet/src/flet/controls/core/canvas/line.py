from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Line")
class Line(Shape):
    """
    Draws a line between the given points using the given paint. The line is stroked,
    the value of the `Paint.style` is ignored.
    """

    x1: OptionalNumber = None
    """
    The x-axis coordinate of the line's starting point.
    """

    y1: OptionalNumber = None
    """
    The y-axis coordinate of the line's starting point.
    """

    x2: OptionalNumber = None
    """
    The x-axis coordinate of the line's end point.
    """

    y2: OptionalNumber = None
    """
    The y-axis coordinate of the line's end point.
    """

    paint: Optional[Paint] = None
    """
    A style to draw a line with. The value of this property is the instance of
    [`Paint`](https://flet.dev/docs/reference/types/paint) class.
    """

