from typing import Optional

import flet as ft
from flet_shadcn_ui.types import BadgeVariant

__all__ = ["Badge"]


@ft.control("ShadBadge")
class Badge(ft.LayoutControl):
    """
    A Shadcn badge: a small label for a status, a tag or a count.

    Example:
    ```python
    shad.Badge("New")
    shad.Badge("Failed", variant=shad.BadgeVariant.DESTRUCTIVE)
    ```
    """

    content: ft.StrOrControl
    """
    The label of this badge.

    If a string is provided, it is wrapped in a :class:`~flet.Text` control.
    """

    variant: BadgeVariant = BadgeVariant.PRIMARY
    """
    The visual variant of this badge.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The background color.

    If `None`, the color is taken from :attr:`variant`.
    """

    hover_bgcolor: Optional[ft.ColorValue] = None
    """
    The background color while the pointer hovers over this badge.
    """

    color: Optional[ft.ColorValue] = None
    """
    The color of the label.

    If `None`, the color is taken from :attr:`variant`.
    """

    on_click: Optional[ft.ControlEventHandler["Badge"]] = None
    """
    Called when this badge is clicked.
    """
