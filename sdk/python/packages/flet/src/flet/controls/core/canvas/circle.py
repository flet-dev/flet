from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Circle")
class Circle(Shape):
    """
    Draws a circle.
    """

    x: OptionalNumber = None
    """
    The x-axis coordinate of the circle's center point.
    """

    y: OptionalNumber = None
    """
    The y-axis coordinate of the circle's center point.
    """

    radius: OptionalNumber = None
    """
    Circle's radius.
    """

    paint: Optional[Paint] = None
    """
    A style to draw a circle with. The value of this property is the instance of
    [`Paint`](https://flet.dev/docs/reference/types/paint) class.
    """

