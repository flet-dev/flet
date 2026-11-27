from dataclasses import field
from typing import Optional

import flet as ft

__all__ = ["BarChartRodStackItem"]


@ft.control("BarChartRodStackItem")
class BarChartRodStackItem(ft.BaseControl):
    """
    Colored segment used to build a stacked bar rod.
    """

    from_y: ft.Number = 0
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

    Defaults to the color of the parent rod.
    """

    gradient: Optional[ft.Gradient] = None
    """
    The gradient this item is filled with.

    Takes precedence over :attr:`color`.
    """

    label: Optional[str] = None
    """
    The text drawn in the middle of this item.

    It is drawn only if it fits within the item's height.
    """

    label_style: Optional[ft.TextStyle] = None
    """
    The text style of the :attr:`label`.

    Defaults to bold, 12-pixel white text.
    """

    border_side: ft.BorderSide = field(default_factory=lambda: ft.BorderSide.none())
    """
    A border around this item.
    """
