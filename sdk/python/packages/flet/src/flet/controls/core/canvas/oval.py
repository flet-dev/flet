from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import Number


@control("Oval")
class Oval(Shape):
    """
    Draws an axis-aligned oval that fills the given axis-aligned rectangle with the
    given `Paint`. Whether the oval is filled or stroked (or both) is controlled by
    `Paint.style`.
    """

    x: Optional[Number] = None
    """
    The x-axis coordinate of the oval's top left point.
    """

    y: Optional[Number] = None
    """
    The y-axis coordinate of the oval's top left point.
    """

    width: Optional[Number] = None
    """
    Width of the rectangle containing the oval.
    """

    height: Optional[Number] = None
    """
    Height of the rectangle containing the oval.
    """

    paint: Optional[Paint] = None
    """
    A style to draw an oval with. The value of this property is the instance of
    [`Paint`][flet.Paint] class.
    """
