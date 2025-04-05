from typing import List, Optional

from flet.controls.control import control
from flet.controls.core.canvas.path import Path
from flet.controls.core.canvas.shape import Shape
from flet.controls.types import OptionalColorValue, OptionalNumber


@control("Shadow")
class Shadow(Shape):
    path: Optional[List[Path.PathElement]] = None
    color: OptionalColorValue = None
    elevation: OptionalNumber = None
    transparent_occluder: Optional[bool] = None
