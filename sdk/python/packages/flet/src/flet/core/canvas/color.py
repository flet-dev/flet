from typing import Optional

from flet.core.canvas.shape import Shape
from flet.core.control import control
from flet.core.types import BlendMode


@control("Color")
class Color(Shape):
    color: OptionalColorValue = None
    blend_mode: Optional[BlendMode] = None
