import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    OptionalColorValue,
    StrOrControl,
    UrlTarget,
)

__all__ = ["OutlinedButton"]


@control("OutlinedButton")
class OutlinedButton(ConstrainedControl, AdaptiveControl):
    """
    Outlined buttons are medium-emphasis buttons. They contain actions that are
    important, but aren’t the primary action in an app. Outlined buttons pair well with
    filled buttons to indicate an alternative, secondary action.

    Online docs: https://flet.dev/docs/controls/outlinedbutton
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
    The value is an instance of [`ButtonStyle`](https://flet.dev/docs/reference/types/buttonstyle) 
    class.
    """

    autofocus: bool = False
    """
    True if the control will be selected as the initial focus.

    If there is more than one control on a page with autofocus set, then the first one
    added to the page will get focus.
    """

    clip_behavior: ClipBehavior = ClipBehavior.NONE
    """
    The content will be clipped (or not) according to this option.

    Value is of type [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) 
    and defaults to `ClipBehavior.NONE`.
    """

    url: Optional[str] = None
    """
    The URL to open when the button is clicked.

    If registered, `on_click` event is fired after that.
    """

    url_target: Optional[UrlTarget] = None
    """
    Where to open URL in the web mode.

    Value is of type [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget) and 
    defaults to `UrlTarget.BLANK`.
    """

    on_click: OptionalControlEventHandler["OutlinedButton"] = None
    """
    Fires when a user clicks the button.
    """

    on_long_press: OptionalControlEventHandler["OutlinedButton"] = None
    """
    Fires when the button is long-pressed.
    """

    on_hover: OptionalControlEventHandler["OutlinedButton"] = None
    """
    Fires when a mouse pointer enters or exists the button response area.

    `data` property of event object contains `true` (string) when cursor enters and
    `false` when it exits.
    """

    on_focus: OptionalControlEventHandler["OutlinedButton"] = None
    """
    Fires when the control has received focus.
    """

    on_blur: OptionalControlEventHandler["OutlinedButton"] = None
    """
    Fires when the control has lost focus.
    """

    def before_update(self):
        super().before_update()
        assert (
            self.icon
            or isinstance(self.content, str)
            or (isinstance(self.content, Control) and self.content.visible)
        ), "at minimum, icon or a visible content must be provided"

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
