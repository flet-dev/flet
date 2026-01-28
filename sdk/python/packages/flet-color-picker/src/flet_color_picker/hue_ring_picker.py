from typing import Optional

import flet as ft

__all__ = ["HueRingPicker"]


@ft.control("HueRingPicker")
class HueRingPicker(ft.LayoutControl):
    """
    A hue ring color picker control based on flutter_colorpicker.
    """

    picker_color: Optional[ft.ColorValue] = None
    """
    The currently selected color.
    """

    on_color_change: Optional[ft.ControlEventHandler["HueRingPicker"]] = None
    """
    Called when the picker color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """
