from typing import Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Circle")
class Circle(Shape):
    x: OptionalNumber = None
    y: OptionalNumber = None
    radius: OptionalNumber = None
    paint: Optional[Paint] = None
