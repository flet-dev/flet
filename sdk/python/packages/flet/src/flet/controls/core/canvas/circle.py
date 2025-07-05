from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number


@control("Circle")
class Circle(Shape):
    """
    Draws a circle.
    """

    x: Optional[Number] = None
    """
    The x-axis coordinate of the circle's center point.
    """

    y: Optional[Number] = None
    """
    The y-axis coordinate of the circle's center point.
    """

    radius: Optional[Number] = None
    """
    Circle's radius.
    """

    paint: Optional[Paint] = None
    """
    A style to draw a circle with. The value of this property is the instance of
    [`Paint`][flet.Paint] class.
    """
