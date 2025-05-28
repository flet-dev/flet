from dataclasses import field
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control import Control
from flet.controls.core.charts.bar_chart_rod import BarChartRod
from flet.controls.types import OptionalNumber


@control("g")
class BarChartGroup(Control):
    x: int
    """
    Group position on X axis.
    """

    bar_rods: list[BarChartRod] = field(default_factory=list)
    """
    The list of [`BarChartRod`](https://flet.dev/docs/reference/types/barchartrod)
    objects to display in the group.
    """

    group_vertically: Optional[bool] = None
    """
    If set to `True` bar rods are drawn on top of each other; otherwise bar rods
    are drawn next to each other.

    Defaults to `False`.
    """

    bars_space: OptionalNumber = None
    """
    The gap between bar rods.
    """

