from typing import Optional

import flet as ft

__all__ = ["ColorPicker"]


@ft.control("ColorPicker")
class ColorPicker(ft.LayoutControl):
    """
    A color picker control based on flutter_colorpicker.
    """

    picker_color: Optional[ft.ColorValue] = None
    """
    The currently selected color.
    """

    color_picker_width: Optional[ft.Number] = None
    """
    Width of the color picker in virtual pixels.
    """

    on_color_change: Optional[ft.ControlEventHandler["ColorPicker"]] = None
    """
    Called when the picker color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """
