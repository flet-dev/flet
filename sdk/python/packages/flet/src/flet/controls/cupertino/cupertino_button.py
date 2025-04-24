import asyncio
from enum import Enum
from typing import Optional

from flet.controls.alignment import OptionalAlignment
from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    IconValueOrControl,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    StrOrControl,
    UrlTarget,
)

__all__ = ["CupertinoButton", "CupertinoButtonSize"]


class CupertinoButtonSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@control("CupertinoButton")
class CupertinoButton(ConstrainedControl):
    """
    An iOS-style button.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinobutton
    """

    content: Optional[StrOrControl] = None
    icon: Optional[IconValueOrControl] = None
    icon_color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    color: OptionalColorValue = None
    disabled_bgcolor: OptionalColorValue = None
    opacity_on_click: Number = 0.4
    min_size: Number = None
    size_style: CupertinoButtonSize = CupertinoButtonSize.LARGE
    padding: OptionalPaddingValue = None
    alignment: OptionalAlignment = None
    border_radius: BorderRadiusValue = 8.0
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    autofocus: bool = False
    focus_color: OptionalColorValue = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            0 <= self.opacity_on_click <= 1
        ), "opacity_on_click must be between 0 and 1 inclusive"

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
