from dataclasses import field

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number

__all__ = ["Oval"]


@control("Oval")
class Oval(Shape):
    """
    Draws an axis-aligned oval that fills the given
    axis-aligned rectangle with the given [`paint`][(c).].

    The [`style`][flet.Paint.] property of [`paint`][(c).] indicates
    whether this oval is filled, stroked, or both.
    """

    x: Number
    """
    The x-axis coordinate of the oval's top left point.
    """

    y: Number
    """
    The y-axis coordinate of the oval's top left point.
    """

    width: Number = 0
    """
    The width of the rectangle containing the oval.
    """

    height: Number = 0
    """
    The height of the rectangle containing the oval.
    """

    paint: Paint = field(default_factory=lambda: Paint())
    """
    A style to draw an oval with.
    """
