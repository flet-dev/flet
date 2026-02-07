from typing import Optional

import flet as ft

__all__ = ["MaterialPicker"]


@ft.control("MaterialPicker")
class MaterialPicker(ft.LayoutControl):
    """
    A material palette picker for selecting primary and shade colors, with
    optional shade labels.
    """

    picker_color: Optional[ft.ColorValue] = None
    """
    The currently selected color.
    """

    enable_label: bool = False
    """
    Whether to show color shade labels.
    """

    portrait_only: bool = False
    """
    Whether to force portrait layout.
    """

    on_color_change: Optional[ft.ControlEventHandler["MaterialPicker"]] = None
    """
    Called when the picker color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """

    on_primary_change: Optional[ft.ControlEventHandler["MaterialPicker"]] = None
    """
    Called when the primary color is changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the color value as a hex string.
    """
