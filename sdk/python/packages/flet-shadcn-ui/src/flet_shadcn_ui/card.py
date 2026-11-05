from typing import Optional

import flet as ft

__all__ = ["Card"]


@ft.control("ShadCard")
class Card(ft.LayoutControl):
    """
    A Shadcn card with an optional header, content and footer.

    Example:
    ```python
    shad.Card(
        title="Notifications",
        description="You have 3 unread messages.",
        content=ft.Text("..."),
        footer=shad.Button("Mark all as read"),
    )
    ```
    """

    title: Optional[ft.StrOrControl] = None
    """
    The title shown at the top of this card.
    """

    description: Optional[ft.StrOrControl] = None
    """
    The description shown below :attr:`title`.
    """

    content: Optional[ft.Control] = None
    """
    The main content of this card.
    """

    footer: Optional[ft.Control] = None
    """
    The control shown at the bottom of this card.
    """

    leading: Optional[ft.Control] = None
    """
    A control shown before the column of :attr:`title`, :attr:`description`,
    :attr:`content` and :attr:`footer`.
    """

    trailing: Optional[ft.Control] = None
    """
    A control shown after the column of :attr:`title`, :attr:`description`,
    :attr:`content` and :attr:`footer`.
    """

    padding: Optional[ft.PaddingValue] = None
    """
    The space between the border of this card and its contents.

    If `None`, defaults to `24` on every side.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The background color.

    If `None`, the card color of the theme is used.
    """

    border_radius: Optional[ft.BorderRadiusValue] = None
    """
    The corner radius.

    If `None`, the theme radius is used.
    """
