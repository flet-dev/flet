from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.types import OptionalNumber


@control("l")
class ChartAxisLabel(Control):
    value: OptionalNumber = None
    label: Optional[Control] = None
