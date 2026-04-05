from dataclasses import field

from flet.controls.base_control import control
from flet.controls.colors import Colors
from flet.controls.core.canvas.path import Path
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import ColorValue, Number

__all__ = ["Shadow"]


@control("Shadow")
class Shadow(Shape):
    """
    Draws a shadow for a :attr:`path` representing the given material \
    :attr:`elevation`.

    Note:
        The :attr:`transparent_occluder` argument should
        be `True` if the occluding object is not opaque.
    """

    path: list[Path.PathElement] = field(default_factory=list)
    """
    The list of elements describing the path of this shape.
    """

    color: ColorValue = Colors.BLACK
    """
    The shadow's color.
    """

    elevation: Number = 0
    """
    The shadow's elevation.
    """

    transparent_occluder: bool = False
    """
    Whether the occluding object is transparent (not opaque).
    """
