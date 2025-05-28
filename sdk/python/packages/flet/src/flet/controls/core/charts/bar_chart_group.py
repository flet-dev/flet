from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.core.charts.bar_chart_rod import BarChartRod
from flet.controls.types import OptionalNumber


@control("g")
class BarChartGroup(Control):
    x: int
    bar_rods: list[BarChartRod] = field(default_factory=list)
    group_vertically: Optional[bool] = None
    bars_space: OptionalNumber = None
