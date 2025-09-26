from dataclasses import field

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number

__all__ = ["Line"]


@control("Line")
class Line(Shape):
    """
    Draws a line between the given points using the given paint.

    Note:
        The line is always rendered as a stroke, regardless of the value
        of [`paint`][(c).]'s [`style`][flet.Paint.] property.
    """

    x1: Number
    """
    The x-axis coordinate of the line's starting point.
    """

    y1: Number
    """
    The y-axis coordinate of the line's starting point.
    """

    x2: Number
    """
    The x-axis coordinate of the line's end point.
    """

    y2: Number
    """
    The y-axis coordinate of the line's end point.
    """

    paint: Paint = field(default_factory=lambda: Paint())
    """
    A style to draw a line with.
    """
