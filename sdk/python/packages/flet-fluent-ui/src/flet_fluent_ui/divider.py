from typing import Optional

import flet as ft

__all__ = ["Divider"]


@ft.control("FluentDivider")
class Divider(ft.LayoutControl):
    """
    A Fluent divider: a thin line that separates content.

    Example:
    ```python
    ft.Column([ft.Text("Above"), fluent.Divider(), ft.Text("Below")])
    ```
    """

    vertical: bool = False
    """
    Whether the line is vertical, for separating controls in a row.
    """

    size: Optional[ft.Number] = None
    """
    The length of the line.

    If `None`, the line fills the available width (or height, when
    :attr:`vertical`).

    The theme adds a 10 pixel margin at each end of the line, so a vertical
    divider in a row is 20 pixels taller than :attr:`size`.
    """

    thickness: Optional[ft.Number] = None
    """
    The thickness of the line.

    If `None`, the theme's divider thickness (`1`) is used.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the line.

    If `None`, the theme's divider color is used.
    """
