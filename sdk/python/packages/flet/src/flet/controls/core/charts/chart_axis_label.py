from typing import Optional

from flet.controls.control import Control, control
from flet.controls.types import OptionalNumber


@control("l")
class ChartAxisLabel(Control):
    value: OptionalNumber = None
    label: Optional[Control] = None
