from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.path import Path
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import OptionalColorValue, OptionalNumber


@control("Shadow")
class Shadow(Shape):
    """
    Draws a shadow for a `path` representing the given material `elevation`.

    The `transparent_occluder` argument should be `True` if the occluding object
    is not opaque.
    """

    path: Optional[list[Path.PathElement]] = None
    """
    The list of `Path.PathElement` objects describing the path.
    """

    color: OptionalColorValue = None
    """
    Shadow [color](https://flet.dev/docs/reference/colors).
    """

    elevation: OptionalNumber = None
    """
    Shadow elevation.
    """

    transparent_occluder: bool = False
    """
    `True` if the occluding object is not opaque.

    Defaults to `False`.
    """
