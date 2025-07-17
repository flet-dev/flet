from dataclasses import field

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number

__all__ = ["Circle"]


@control("Circle")
class Circle(Shape):
    """
    Draws a circle.
    """

    x: Number
    """
    The x-axis coordinate of the circle's center point.
    """

    y: Number
    """
    The y-axis coordinate of the circle's center point.
    """

    radius: Number = 0
    """
    Circle's radius.
    """

    paint: Paint = field(default_factory=lambda: Paint())
    """
    A style to draw a circle with.
    """
