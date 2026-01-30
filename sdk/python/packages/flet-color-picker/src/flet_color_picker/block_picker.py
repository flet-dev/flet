from typing import Optional

import flet as ft

__all__ = ["BlockPicker"]


@ft.control("BlockPicker")
class BlockPicker(ft.LayoutControl):
    """
    A block color picker control based on flutter_colorpicker.
    """

    picker_color: Optional[ft.ColorValue] = None
    """
    The currently selected color.
    """

    available_colors: Optional[list[ft.ColorValue]] = None
    """
    A list of available colors to pick from.
    """

    use_in_show_dialog: bool = True
    """
    Whether to show the currently selected color when used in a dialog.
    """

    on_color_change: Optional[ft.ControlEventHandler["BlockPicker"]] = None
    """
    Called when the picker color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """
