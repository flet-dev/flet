from dataclasses import field

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number

__all__ = ["Arc"]


@control("Arc")
class Arc(Shape):
    """
    Draws an arc scaled to fit inside the given rectangle.

    It starts from [`start_angle`][(c).] radians around the oval up to [`start_angle`][(c).] +
    [`sweep_angle`][(c).] radians around the oval, with zero radians being the point on
    the right hand side of the oval that crosses the horizontal line that
    intersects the center of the rectangle and with positive angles going
    clockwise around the oval. If [`use_center`][(c).] is `True`, the arc is closed back
    to the center, forming a circle sector. Otherwise, the arc is not closed,
    forming a circle segment.

    https://api.flutter.dev/flutter/dart-ui/Canvas/drawArc.html
    """

    x: Number
    """
    The x-axis coordinate of the arc's top left point.
    """

    y: Number
    """
    The y-axis coordinate of the arc's top left point.
    """

    width: Number = 0
    """
    The width of the rectangle containing the arc's oval.
    """

    height: Number = 0
    """
    The height of the rectangle containing the arc's oval.
    """

    start_angle: Number = 0
    """
    The starting angle in radians to draw arc from.
    """

    sweep_angle: Number = 0
    """
    The length of the arc in radians.
    """

    use_center: bool = False
    """
    Whether this arc is closed back to the center, forming a
    circle sector. If not closed (`False`), this arc forms a circle segment.
    """

    paint: Paint = field(default_factory=lambda: Paint())
    """
    A style to draw an arc with.
    """
