from typing import Any, Optional

from flet.controls.base_control import control
from flet.controls.core.canvas.shape import Shape
from flet.controls.painting import Paint


@control("Fill")
class Fill(Shape):
    paint: Optional[Paint] = None
