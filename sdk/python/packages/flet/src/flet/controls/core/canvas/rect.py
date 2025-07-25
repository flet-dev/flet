from dataclasses import field

from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadius, BorderRadiusValue
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number

__all__ = ["Rect"]


@control("Rect")
class Rect(Shape):
    """
    Draws a rectangle.
    """

    x: Number
    """
    The x-axis coordinate of this rectangle's top left point.
    """

    y: Number
    """
    The y-axis coordinate of this rectangle's top left point.
    """

    width: Number = 0
    """
    The width of this rectangle.
    """

    height: Number = 0
    """
    The height of this rectangle.
    """

    border_radius: BorderRadiusValue = field(
        default_factory=lambda: BorderRadius.all(0)
    )
    """
    The border radius of this rectangle.
    """

    paint: Paint = field(default_factory=lambda: Paint())
    """
    A style to draw this rectangle with.
    """
