import asyncio
from typing import Optional

from flet.controls.adaptive_control import AdaptiveControl
from flet.controls.base_control import control
from flet.controls.buttons import ButtonStyle
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.types import (
    ClipBehavior,
    IconValueOrControl,
    OptionalColorValue,
    OptionalControlEventCallable,
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
    icon: Optional[IconValueOrControl] = None
    icon_color: OptionalColorValue = None
    style: Optional[ButtonStyle] = None
    autofocus: bool = False
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    clip_behavior: Optional[ClipBehavior] = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_hover: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
