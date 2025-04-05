from typing import Optional

from flet.controls.control import Control, control
from flet.controls.types import OptionalNumber


@control("g")
class BarChartGroup(Control):
    group_vertically: Optional[bool] = None
    bars_space: OptionalNumber = None
