from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["BarChartRodStackItem"]


@ft.control("BarChartRodStackItem")
class BarChartRodStackItem(ft.BaseControl):
    from_y: Optional[ft.Number] = None
    """
    The starting position of this item inside a bar rod.
    """

    to_y: ft.Number = 0
    """
    The ending position of this item inside a bar rod.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of this item.
    """

    border_side: ft.BorderSide = field(default_factory=lambda: ft.BorderSide.none())
    """
    A border around this item.
    """
