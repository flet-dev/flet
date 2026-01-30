from typing import Optional

import flet as ft

__all__ = ["MultipleChoiceBlockPicker"]


@ft.control("MultipleChoiceBlockPicker")
class MultipleChoiceBlockPicker(ft.LayoutControl):
    """
    A multiple choice block color picker control based on flutter_colorpicker.
    """

    picker_colors: Optional[list[ft.ColorValue]] = None
    """
    The currently selected colors.
    """

    available_colors: Optional[list[ft.ColorValue]] = None
    """
    A list of available colors to pick from.
    """

    on_colors_change: Optional[ft.ControlEventHandler["MultipleChoiceBlockPicker"]] = (
        None
    )
    """
    Called when the picker colors are changed.

    The [`data`][flet.Event.data] property of the event handler argument contains
    the list of color values as hex strings.
    """
