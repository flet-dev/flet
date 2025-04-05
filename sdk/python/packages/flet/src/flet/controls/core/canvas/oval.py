from typing import Optional

from flet.controls.control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Oval")
class Oval(Shape):
    x: OptionalNumber = None
    y: OptionalNumber = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    paint: Optional[Paint] = None
