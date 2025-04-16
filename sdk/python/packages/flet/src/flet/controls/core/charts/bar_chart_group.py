from dataclasses import field
from typing import List, Optional

from flet.controls.control import Control, control
from flet.controls.core.charts.bar_chart_rod import BarChartRod
from flet.controls.types import OptionalNumber


@control("g")
class BarChartGroup(Control):
    x: int
    bar_rods: List[BarChartRod] = field(default_factory=list)
    group_vertically: Optional[bool] = None
    bars_space: OptionalNumber = None
