import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.types import (
    ClipBehavior,
    ColorValue,
    IconValueOrControl,
    StrOrControl,
    UrlTarget,
)

__all__ = ["TextButton"]


@control("TextButton")
class TextButton(ConstrainedControl, AdaptiveControl):
    """
    Text buttons are used for the lowest priority actions, especially when presenting
    multiple options. Text buttons can be placed on a variety of backgrounds. Until the
    button is interacted with, its container isn’t visible.
    """

    content: Optional[StrOrControl] = None
    """
    A Control representing custom button content.
    """

    icon: Optional[IconValueOrControl] = None
    """
    Icon shown in the button.
    """

    icon_color: Optional[ColorValue] = None
    """
    Icon color.
    """

    style: Optional[ButtonStyle] = None
    """
    TBD
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first one
    added to the page will get focus.
    """

    url: Optional[str] = None
    """
    The URL to open when the button is clicked.

    If registered, [`on_click`][flet.TextButton.on_click] event is fired after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option.
    """

    on_click: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when a user clicks the button.
    """

    on_long_press: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when the button is long-pressed.
    """

    on_hover: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when a mouse pointer enters or exists the button response area.

    `data` property of event object is `True` when cursor enters and
    `False` when it exits.
    """

    on_focus: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when the control has received focus.
    """

    on_blur: Optional[ControlEventHandler["TextButton"]] = None
    """
    Called when the control has lost focus.
    """

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
