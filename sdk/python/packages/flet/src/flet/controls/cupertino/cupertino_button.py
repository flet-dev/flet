import asyncio
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    IconValue,
    IconValueOrControl,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    StrOrControl,
    UrlTarget,
)
from flet.utils.deprecated import deprecated_warning

__all__ = ["CupertinoButton"]


@control("CupertinoButton")
class CupertinoButton(ConstrainedControl):
    """
    An iOS-style button.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinobutton
    """

    def __setattr__(self, name, value):
        if name == "text" and value is not None:
            deprecated_warning(
                name="text",
                reason="Use content instead.",
                version="0.70.0",
                delete_version="0.70.3",
            )
        super().__setattr__(name, value)

    content: Optional[StrOrControl] = None
    icon: Optional[IconValueOrControl] = None
    icon_color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    color: OptionalColorValue = None
    disabled_bgcolor: OptionalColorValue = None
    opacity_on_click: Number = 0.4
    min_size: Number = None
    padding: OptionalPaddingValue = None
    alignment: Optional[Alignment] = None
    border_radius: OptionalBorderRadiusValue = 8.0
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    autofocus: bool = False
    focus_color: OptionalColorValue = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None
    text: Optional[str] = None  # deprecated

    def before_update(self):
        super().before_update()
        assert (
            0 <= self.opacity_on_click <= 1
        ), "opacity_on_click must be between 0 and 1 inclusive"

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
