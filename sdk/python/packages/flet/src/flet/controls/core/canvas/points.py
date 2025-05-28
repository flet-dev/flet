from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.transform import OffsetValue


class PointMode(Enum):
    """
    Defines how a list of points is interpreted when drawing a set of points.
    """

    POINTS = "points"
    """
    Draw each point separately. If the `Paint.stroke_cap` is `StrokeCap.ROUND`,
    then each point is drawn as a circle with the diameter of the `Paint.stroke_width`,
    filled as described by the `Paint` (ignoring `Paint.style`). Otherwise, each point
    is drawn as an axis-aligned square with sides of length `Paint.stroke_width`, filled
    as described by the `Paint` (ignoring `Paint.style`).
    """

    LINES = "lines"
    """
    Draw each sequence of two points as a line segment. If the number of points is odd,
    then the last point is ignored. The lines are stroked as described by the `Paint`
    (ignoring `Paint.style`).
    """

    POLYGON = "polygon"
    """
    Draw the entire sequence of point as one line. The lines are stroked as described
    by the `Paint` (ignoring `Paint.style`).
    """


@control("Points")
class Points(Shape):
    """
    Draws a sequence of points according to the given `point_mode`.
    """

    points: Optional[list[OffsetValue]] = None
    """
    The list of `ft.Offset` describing points.
    """

    point_mode: Optional[PointMode] = None
    """
    Defines how a list of points is interpreted when drawing a set of points.

    Value is of type [`PointMode`](https://flet.dev/docs/reference/types/pointmode).
    """

    paint: Optional[Paint] = None
    """
    A style to draw points with. The value of this property is the instance of
    [`Paint`](https://flet.dev/docs/reference/types/paint) class.
    """

