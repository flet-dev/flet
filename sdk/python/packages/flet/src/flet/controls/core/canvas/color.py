from typing import Optional

from flet.controls.control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import BlendMode, OptionalColorValue


@control("Color")
class Color(Shape):
    color: OptionalColorValue = None
    blend_mode: Optional[BlendMode] = None
