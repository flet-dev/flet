from typing import Optional

from flet.controls.control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Line")
class Line(Shape):
    x1: OptionalNumber = None
    y1: OptionalNumber = None
    x2: OptionalNumber = None
    y2: OptionalNumber = None
    paint: Optional[Paint] = None
