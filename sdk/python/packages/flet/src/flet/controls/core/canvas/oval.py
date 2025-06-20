from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Oval")
class Oval(Shape):
    """
    Draws an axis-aligned oval that fills the given axis-aligned rectangle with the
    given `Paint`. Whether the oval is filled or stroked (or both) is controlled by
    `Paint.style`.
    """

    x: OptionalNumber = None
    """
    The x-axis coordinate of the oval's top left point.
    """

    y: OptionalNumber = None
    """
    The y-axis coordinate of the oval's top left point.
    """

    width: OptionalNumber = None
    """
    Width of the rectangle containing the oval.
    """

    height: OptionalNumber = None
    """
    Height of the rectangle containing the oval.
    """

    paint: Optional[Paint] = None
    """
    A style to draw an oval with. The value of this property is the instance of
    [`Paint`](https://flet.dev/docs/reference/types/paint) class.
    """

