from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint
from flet.controls.types import OptionalNumber


@control("Rect")
class Rect(Shape):
    x: OptionalNumber = None
    y: OptionalNumber = None
    width: OptionalNumber = None
    height: OptionalNumber = None
    border_radius: OptionalBorderRadiusValue = None
    paint: Optional[Paint] = None
