import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    OptionalColorValue,
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

    Online docs: https://flet.dev/docs/controls/textbutton
    """

    content: Optional[StrOrControl] = None
    """
    A Control representing custom button content.
    """

    icon: Optional[IconValueOrControl] = None
    """
    Icon shown in the button.
    """

    icon_color: OptionalColorValue = None
    """
    Icon [color](https://flet.dev/docs/reference/colors).
    """

    style: Optional[ButtonStyle] = None
    """
    Value is of type [`ButtonStyle`](https://flet.dev/docs/reference/types/buttonstyle).
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

    If registered, `on_click` event is fired after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of type [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget).
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior)
    and defaults to `ClipBehavior.NONE`.
    """

    on_click: OptionalControlEventHandler["TextButton"] = None
    """
    Fires when a user clicks the button.
    """

    on_long_press: OptionalControlEventHandler["TextButton"] = None
    """
    Fires when the button is long-pressed.
    """

    on_hover: OptionalControlEventHandler["TextButton"] = None
    """
    Fires when a mouse pointer enters or exists the button response area.

    `data` property of event object contains `true` (string) when cursor enters and
    `false` when it exits.
    """

    on_focus: OptionalControlEventHandler["TextButton"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["TextButton"] = None
    """
    Fires when the control has lost focus.
    """

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
