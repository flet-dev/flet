from typing import Optional

import flet as ft

__all__ = ["HueRingPicker"]


@ft.control("HueRingPicker")
class HueRingPicker(ft.LayoutControl):
    """
    A hue ring color picker that lets users select a hue on a circular ring,
    with an optional alpha slider.
    """

    picker_color: Optional[ft.ColorValue] = None
    """
    The currently selected color.
    """

    color_picker_height: Optional[ft.Number] = None
    """
    Height of the color picker in virtual pixels.
    """

    enable_alpha: bool = False
    """
    Whether to enable alpha (opacity) slider.
    """

    hue_ring_stroke_width: Optional[ft.Number] = None
    """
    Stroke width for the hue ring.
    """

    picker_area_border_radius: Optional[ft.BorderRadiusValue] = None
    """
    Border radius for the picker area.
    """

    portrait_only: bool = False
    """
    Whether to force portrait layout.
    """

    on_color_change: Optional[ft.ControlEventHandler["HueRingPicker"]] = None
    """
    Called when the picker color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """
