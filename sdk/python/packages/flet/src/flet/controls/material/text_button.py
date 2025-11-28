from typing import Optional, Union

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.control_event import ControlEventHandler
from flet.controls.layout_control import LayoutControl
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    IconDataOrControl,
    StrOrControl,
    Url,
)

__all__ = ["TextButton"]


@control("TextButton")
class TextButton(LayoutControl, AdaptiveControl):
    """
    Text buttons are used for the lowest priority actions, especially when presenting
    multiple options. Text buttons can be placed on a variety of backgrounds. Until the
    button is interacted with, its container isn’t visible.

    ```python
    ft.TextButton(
        content="Text Button",
        icon=ft.Icons.STAR_BORDER,
        icon_color=ft.Colors.BLUE_300,
    )
    ```
    """

    content: Optional[StrOrControl] = None
    """
    A Control representing custom button content.
    """

    icon: Optional[IconDataOrControl] = None
    """
    An icon to show in this button.
    """

    icon_color: Optional[ColorValue] = None
    """
    Icon color.
    """

    style: Optional[ButtonStyle] = None
    """
    Defines the style of this button.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first one
    added to the page will get focus.
    """

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][(c).] event callback is
    provided, it is fired after that.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    Defines how the content of this button is clipped.
    """

    on_click: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when a user clicks this button.
    """

    on_long_press: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when this button is long-pressed.
    """

    on_hover: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when a mouse pointer enters or exists this button's response area.

    The [`data`][flet.Event.] property of the event handler argument is `True` when
    cursor enters and `False` when it exits.
    """

    on_focus: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when this button has received focus.
    """

    on_blur: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when this button has lost focus.
    """

    async def focus(self):
        await self._invoke_method("focus")
