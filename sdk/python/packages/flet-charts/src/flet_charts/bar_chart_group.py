from dataclasses import field
from typing import Optional

import flet as ft
from flet_charts.bar_chart_rod import BarChartRod

__all__ = ["BarChartGroup"]


@ft.control("BarChartGroup")
class BarChartGroup(ft.BaseControl):
    x: int = 0
    """
    Group position on X axis.
    """

    rods: list[BarChartRod] = field(default_factory=list)
    """
    The list of [`BarChartRod`][(p).]
    objects to display in the group.
    """

    group_vertically: bool = False
    """
    If set to `True` bar rods are drawn on top of each other; otherwise bar rods
    are drawn next to each other.
    """

    spacing: Optional[ft.Number] = None
    """
    The amount of space between bar rods.
    """
