from dataclasses import dataclass
from enum import Enum
from typing import Optional

import flet as ft

__all__ = ["ColorLabelType", "ColorPicker", "HsvColor", "PaletteType"]


class ColorLabelType(Enum):
    HEX = "hex"
    RGB = "rgb"
    HSV = "hsv"
    HSL = "hsl"


class PaletteType(Enum):
    HSV = "hsv"
    HSV_WITH_HUE = "hsvWithHue"
    HSV_WITH_VALUE = "hsvWithValue"
    HSV_WITH_SATURATION = "hsvWithSaturation"
    HSL = "hsl"
    HSL_WITH_HUE = "hslWithHue"
    HSL_WITH_LIGHTNESS = "hslWithLightness"
    HSL_WITH_SATURATION = "hslWithSaturation"
    RGB_WITH_BLUE = "rgbWithBlue"
    RGB_WITH_GREEN = "rgbWithGreen"
    RGB_WITH_RED = "rgbWithRed"
    HUE_WHEEL = "hueWheel"


@dataclass
class HsvColor:
    alpha: ft.Number
    hue: ft.Number
    saturation: ft.Number
    value: ft.Number


@ft.control("ColorPicker")
class ColorPicker(ft.LayoutControl):
    """
    A full-featured color picker with palette, sliders, labels, and optional
    history.
    """

    color: Optional[ft.ColorValue] = None
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
    """

    palette_type: Optional[PaletteType] = None
    """
    Palette type for the picker area.
    """

    picker_area_border_radius: Optional[ft.BorderRadiusValue] = None
    """
    Border radius for the picker area.
    """

    picker_area_height_percent: Optional[ft.Number] = None
    """
    Height of the picker area as a percentage of the picker width.
    """

    hsv_color: Optional[HsvColor] = None
    """
    The currently selected HSV color.

    Provide an `HsvColor` instance with fields: `alpha`, `hue`, `saturation`,
    `value`.
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

    on_hsv_color_change: Optional[ft.ControlEventHandler["ColorPicker"]] = None
    """
    Called when the picker HSV color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the HSV values as a dict with keys: `alpha`, `hue`, `saturation`, `value`.
    """
