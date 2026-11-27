from typing import Optional

import flet as ft
from flet_fluent_ui.types import ColorSpectrumShape

__all__ = ["ColorPicker"]


@ft.control("FluentColorPicker")
class ColorPicker(ft.LayoutControl):
    """
    A Fluent color picker: a color spectrum with sliders and text fields to
    pick a color.

    Example:
    ```python
    fluent.ColorPicker(value="#0078d4", show_more_button=False)
    ```
    """

    value: Optional[ft.ColorValue] = None
    """
    The selected color.

    If `None`, the picker starts at Fluent blue (`#0078D4`). After the user
    picks a color, it holds a `#aarrggbb` string.
    """

    horizontal: bool = False
    """
    Whether the inputs are shown next to the spectrum, instead of below it.
    """

    spectrum_shape: ColorSpectrumShape = ColorSpectrumShape.RING
    """
    The shape of the color spectrum.
    """

    show_preview: bool = True
    """
    Whether a swatch of the selected color is shown next to the spectrum.
    """

    show_color_slider: bool = True
    """
    Whether a brightness slider is shown below the spectrum.
    """

    show_more_button: bool = True
    """
    Whether the color channel inputs are hidden behind a "More" button.

    If `False`, the inputs are always shown (if enabled by
    :attr:`show_channel_inputs` and :attr:`show_hex_input`).
    """

    show_channel_inputs: bool = True
    """
    Whether fields for the red, green and blue (or hue, saturation and
    value) channels are shown.
    """

    show_hex_input: bool = True
    """
    Whether a field for the hexadecimal color code is shown.
    """

    alpha_enabled: bool = True
    """
    Whether the color can be partly transparent.
    """

    show_alpha_slider: bool = True
    """
    Whether an opacity slider is shown, when :attr:`alpha_enabled`.
    """

    show_alpha_input: bool = True
    """
    Whether an opacity field is shown, when :attr:`alpha_enabled`.
    """

    min_hue: int = 0
    """
    The smallest hue offered, from `0` to `359`.
    """

    max_hue: int = 359
    """
    The largest hue offered, from `0` to `359`.
    """

    min_saturation: int = 0
    """
    The smallest saturation offered, from `0` to `100`.
    """

    max_saturation: int = 100
    """
    The largest saturation offered, from `0` to `100`.
    """

    min_brightness: int = 0
    """
    The smallest brightness offered, from `0` to `100`.
    """

    max_brightness: int = 100
    """
    The largest brightness offered, from `0` to `100`.
    """

    on_change: Optional[ft.ControlEventHandler["ColorPicker"]] = None
    """
    Called when the user changes the color.

    :attr:`value` holds the new color.
    """
