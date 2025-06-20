from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Arc")
class Arc(Shape):
    """
    Draws an arc scaled to fit inside the given rectangle.

    It starts from `start_angle` radians around the oval up to `start_angle` +
    `sweep_angle` radians around the oval, with zero radians being the point on
    the right hand side of the oval that crosses the horizontal line that
    intersects the center of the rectangle and with positive angles going
    clockwise around the oval. If `use_center` is `True`, the arc is closed back
    to the center, forming a circle sector. Otherwise, the arc is not closed,
    forming a circle segment.

    https://api.flutter.dev/flutter/dart-ui/Canvas/drawArc.html
    """

    x: OptionalNumber = None
    """
    The x-axis coordinate of the arc's top left point.
    """

    y: OptionalNumber = None
    """
    The y-axis coordinate of the arc's top left point.
    """

    width: OptionalNumber = None
    """
    Width of the rectangle containing the arc's oval.
    """

    height: OptionalNumber = None
    """
    Height of the rectangle containing the arc's oval.
    """

    start_angle: OptionalNumber = None
    """
    Starting angle in radians to draw arc from.
    """

    sweep_angle: OptionalNumber = None
    """
    The length of the arc in radians.
    """

    use_center: Optional[bool] = None
    """
    If `use_center` is `True`, the arc is closed back to the center, forming a
    circle sector. Otherwise, the arc is not closed, forming a circle segment.
    """

    paint: Optional[Paint] = None
    """
    A style to draw an arc with. The value of this property is the instance of
    [`Paint`](https://flet.dev/docs/reference/types/paint) class.
    """
