from typing import Optional

import flet as ft

__all__ = ["Card"]


@ft.control("FluentCard")
class Card(ft.LayoutControl):
    """
    A Fluent card: a bordered surface that groups related content.

    Example:
    ```python
    fluent.Card(content=ft.Text("Card content"))
    ```
    """

    content: ft.Control
    """
    The control shown inside this card.
    """

    padding: ft.PaddingValue = 12
    """
    The space between the border and :attr:`content`.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The background color.

    If `None`, the card color of the theme is used.
    """

    border_color: Optional[ft.ColorValue] = None
    """
    The color of the border.

    If `None`, the theme's card stroke color is used.
    """

    border_radius: ft.BorderRadiusValue = 4
    """
    The corner radius.
    """
