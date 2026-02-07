from typing import Optional

import flet as ft

__all__ = ["BlockPicker"]


@ft.control("BlockPicker")
class BlockPicker(ft.LayoutControl):
    """
    A color picker that lets users choose a color from a grid of available
    colors.
    """

    picker_color: Optional[ft.ColorValue] = None
    """
    The currently selected color.
    """

    available_colors: Optional[list[ft.ColorValue]] = None
    """
    A list of available colors to pick from.
    """

    on_color_change: Optional[ft.ControlEventHandler["BlockPicker"]] = None
    """
    Called when the picker color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """
