from typing import Optional

from flet.controls.border import BorderSide
from flet.controls.control import Control, control
from flet.controls.types import OptionalColorValue, OptionalNumber


@control("i")
class BarChartRodStackItem(Control):
    from_y: OptionalNumber = None
    to_y: OptionalNumber = None
    color: OptionalColorValue = None
    border_side: Optional[BorderSide] = None
