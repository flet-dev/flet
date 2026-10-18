from typing import Optional

import flet as ft
from flet_shadcn_ui.types import ButtonVariant

__all__ = ["IconButton"]


@ft.control("ShadIconButton")
class IconButton(ft.LayoutControl):
    """
    A Shadcn button that shows only an icon.

    Example:
    ```python
    shad.IconButton(
        icon=shad.LucideIcons.ROCKET,
        on_click=lambda e: print("launched"),
    )
    ```
    """

    icon: ft.IconDataOrControl
    """
    The icon to show.
    """

    variant: ButtonVariant = ButtonVariant.PRIMARY
    """
    The visual variant of this button.

    :attr:`~flet_shadcn_ui.ButtonVariant.LINK` is not supported and is shown as
    :attr:`~flet_shadcn_ui.ButtonVariant.PRIMARY`.
    """

    icon_size: Optional[ft.Number] = None
    """
    The size of :attr:`icon`.

    If `None`, defaults to `16`.
    """

    bgcolor: Optional[ft.ColorValue] = None
    """
    The background color.

    If `None`, the color is taken from :attr:`variant`.
    """

    hover_bgcolor: Optional[ft.ColorValue] = None
    """
    The background color while the pointer hovers over this button.
    """

    color: Optional[ft.ColorValue] = None
    """
    The icon color.

    If `None`, the color is taken from :attr:`variant`.
    """

    hover_color: Optional[ft.ColorValue] = None
    """
    The icon color while the pointer hovers over this button.
    """

    autofocus: bool = False
    """
    Whether this button should be focused on initial display.
    """

    on_click: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when this button is clicked.
    """

    on_long_press: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when this button is long-pressed.
    """

    on_hover: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when the pointer enters or exits this button.

    The :attr:`~flet.Event.data` property of the event handler argument is
    `True` when the pointer entered, and `False` when it exited.
    """

    on_focus: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when this button receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["IconButton"]] = None
    """
    Called when this button loses focus.
    """

    async def focus(self):
        """
        Requests focus for this button.
        """
        await self._invoke_method("focus")
