from enum import Enum
from typing import Optional

import flet as ft

__all__ = ["ColorLabelType", "ColorPicker"]


class ColorLabelType(Enum):
    HEX = "hex"
    RGB = "rgb"
    HSV = "hsv"
    HSL = "hsl"


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

    color_history: Optional[list[ft.ColorValue]] = None
    """
    A list of colors to display as a history palette.

    To be notified when the palette changes, set `on_history_change`.
    """

    display_thumb_color: bool = True
    """
    Whether to display the thumb color in slider.
    """

    enable_alpha: bool = True
    """
    Whether to enable alpha (opacity) slider.
    """

    hex_input_bar: bool = True
    """
    Whether to show the hex input bar.
    """

    label_text_style: Optional[ft.TextStyle] = None
    """
    Text style for labels.
    """

    label_types: Optional[list[ColorLabelType]] = None
    """
    Color label types to display.

    Values:
        - `ColorLabelType.HEX`
        - `ColorLabelType.RGB`
        - `ColorLabelType.HSV`
        - `ColorLabelType.HSL`
    """

    on_color_change: Optional[ft.ControlEventHandler["ColorPicker"]] = None
    """
    Called when the picker color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """

    on_history_change: Optional[ft.ControlEventHandler["ColorPicker"]] = None
    """
    Called when the history palette is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the list of color values as hex strings.
    """
