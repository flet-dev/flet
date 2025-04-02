from typing import Optional

from flet.core.canvas.shape import Shape
from flet.core.control import control
from flet.core.types import BlendMode, ColorValue


@control("Color")
class Color(Shape):
    color: Optional[ColorValue] = None
    blend_mode: Optional[BlendMode] = None
