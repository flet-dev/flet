from enum import Enum
from typing import Optional

import flet as ft
from flet_color_pickers.color_picker import ColorLabelType

__all__ = ["ColorModel", "SlidePicker"]


class ColorModel(Enum):
    """
    Defines color models.
    """

    RGB = "rgb"
    """Red, green, blue channels."""

    HSV = "hsv"
    """Hue, saturation, value channels."""

    HSL = "hsl"
    """Hue, saturation, lightness channels."""


@ft.control("SlidePicker")
class SlidePicker(ft.LayoutControl):
    """
    A slider-based color picker that exposes RGB/HSV/HSL channels with optional
    labels and indicators.
    """

    color: Optional[ft.ColorValue] = None
    """
    The currently selected color.
    """

    color_model: Optional[ColorModel] = None
    """
    The color model used by the sliders.
    """

    display_thumb_color: bool = True
    """
    Whether to display the thumb color in sliders.
    """

    enable_alpha: bool = True
    """
    Whether to enable alpha (opacity) slider.
    """

    indicator_alignment_begin: Optional[ft.Alignment] = None
    """
    Alignment for the indicator split begin.
    """

    indicator_alignment_end: Optional[ft.Alignment] = None
    """
    Alignment for the indicator split end.
    """

    indicator_border_radius: Optional[ft.BorderRadiusValue] = None
    """
    Border radius for the indicator.
    """

    indicator_size: Optional[ft.Size] = None
    """
    Size of the indicator.
    """

    label_text_style: Optional[ft.TextStyle] = None
    """
    Text style for labels.
    """

    label_types: Optional[list[ColorLabelType]] = None
    """
    Color label types to display.
    """

    show_indicator: bool = True
    """
    Whether to show the color indicator.
    """

    show_label: bool = True
    """
    Whether to show labels.
    """

    show_params: bool = True
    """
    Whether to show parameter values.
    """

    show_slider_text: bool = True
    """
    Whether to show slider text.
    """

    slider_size: Optional[ft.Size] = None
    """
    Size of the sliders.
    """

    slider_text_style: Optional[ft.TextStyle] = None
    """
    Text style for slider text.
    """

    on_color_change: Optional[ft.ControlEventHandler["SlidePicker"]] = None
    """
    Called when the picker color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """
