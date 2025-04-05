from typing import Any, Optional

from flet.controls.control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Arc")
class Arc(Shape):
    x: OptionalNumber = None
    y: OptionalNumber = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    start_angle: OptionalNumber = None
    sweep_angle: OptionalNumber = None
    use_center: Optional[bool] = None
    paint: Optional[Paint] = None
