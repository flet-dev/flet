from typing import Optional

import flet as ft
from flet_shadcn_ui.types import ColorScheme

__all__ = ["Theme"]


@ft.control("ShadTheme")
class Theme(ft.LayoutControl):
    """
    Applies a shadcn theme to its :attr:`content`.

    All `flet_shadcn_ui` controls inside :attr:`content` use this theme.

    Wrapping controls in a `Theme` is optional: a control without a `Theme`
    ancestor uses the :attr:`~flet_shadcn_ui.ColorScheme.SLATE` color scheme and
    follows the page's light or dark mode.

    Example:
    ```python
    shad.Theme(
        color_scheme=shad.ColorScheme.VIOLET,
        content=shad.Button("Themed"),
    )
    ```
    """

    content: ft.Control
    """
    The control to apply the theme to.
    """

    color_scheme: ColorScheme = ColorScheme.SLATE
    """
    The color scheme to use.
    """

    brightness: Optional[ft.Brightness] = None
    """
    Whether to use the light or dark variant of :attr:`color_scheme`.

    If `None`, follows the brightness of the page theme.
    """

    radius: Optional[ft.BorderRadiusValue] = None
    """
    The default corner radius of themed controls.

    If `None`, defaults to `6` on every corner.
    """
