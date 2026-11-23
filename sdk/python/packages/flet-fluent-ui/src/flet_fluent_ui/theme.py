from typing import Optional

import flet as ft

__all__ = ["Theme"]


@ft.control("FluentTheme")
class Theme(ft.LayoutControl):
    """
    Applies a Fluent theme to its :attr:`content`.

    All `flet_fluent_ui` controls inside :attr:`content` use this theme.

    Wrapping controls in a `Theme` is optional: a control without a `Theme`
    ancestor uses the default blue accent color and follows the page's light or
    dark mode.

    Example:
    ```python
    fluent.Theme(
        accent_color=ft.Colors.PURPLE,
        content=fluent.FilledButton("Themed"),
    )
    ```
    """

    content: ft.Control
    """
    The control to apply the theme to.
    """

    accent_color: Optional[ft.ColorValue] = None
    """
    The accent color, used for filled buttons, checked checkboxes and switches,
    sliders, progress indicators and focus highlights.

    Lighter and darker shades for hover and pressed states are derived from it.

    If `None`, Fluent's default blue is used.
    """

    brightness: Optional[ft.Brightness] = None
    """
    Whether to use the light or dark Fluent theme.

    If `None`, follows the brightness of the page theme.
    """

    font_family: Optional[str] = None
    """
    The font family of the text in themed controls.

    If `None`, Fluent's default (`Segoe UI Variable` on Windows) is used.
    """
