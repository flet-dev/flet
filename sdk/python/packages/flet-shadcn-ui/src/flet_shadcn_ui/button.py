from typing import Optional

import flet as ft
from flet_shadcn_ui.types import ButtonSize, ButtonVariant

__all__ = ["Button"]


@ft.control("ShadButton")
class Button(ft.LayoutControl):
    """
    A shadcn/ui button.

    Example:
    ```python
    shad.Button("Save", on_click=lambda e: print("saved"))
    shad.Button("Delete", variant=shad.ButtonVariant.DESTRUCTIVE)
    ```
    """

    content: Optional[ft.StrOrControl] = None
    """
    The button's label.

    If a string is provided, it is wrapped in a :class:`~flet.Text` control.
    """

    leading: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown before :attr:`content`.
    """

    trailing: Optional[ft.IconDataOrControl] = None
    """
    An icon or control shown after :attr:`content`.
    """

    variant: ButtonVariant = ButtonVariant.PRIMARY
    """
    The visual variant of this button.
    """

    size: ButtonSize = ButtonSize.REGULAR
    """
    The size of this button.
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
    The foreground (text and icon) color.

    If `None`, the color is taken from :attr:`variant`.
    """

    hover_color: Optional[ft.ColorValue] = None
    """
    The foreground color while the pointer hovers over this button.
    """

    gap: Optional[ft.Number] = None
    """
    The space between :attr:`leading`, :attr:`content` and :attr:`trailing`.

    If `None`, defaults to `8`.
    """

    autofocus: bool = False
    """
    Whether this button should be focused on initial display.
    """

    on_click: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when this button is clicked.
    """

    on_long_press: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when this button is long-pressed.
    """

    on_hover: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when the pointer enters or exits this button.

    The :attr:`~flet.Event.data` property of the event handler argument is
    `True` when the pointer entered, and `False` when it exited.
    """

    on_focus: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when this button receives focus.
    """

    on_blur: Optional[ft.ControlEventHandler["Button"]] = None
    """
    Called when this button loses focus.
    """

    async def focus(self):
        """
        Requests focus for this button.
        """
        await self._invoke_method("focus")
