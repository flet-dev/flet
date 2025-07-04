import asyncio
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    IconValueOrControl,
    Number,
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
    Icon [color](https://flet.dev/docs/reference/colors).
    """

    bgcolor: Optional[ColorValue] = None
    """
    Button's background [color](https://flet.dev/docs/reference/colors).
    """

    color: Optional[ColorValue] = None
    """
    Button's text [color](https://flet.dev/docs/reference/colors).
    """

    disabled_bgcolor: Optional[ColorValue] = None
    """
    The background [color](https://flet.dev/docs/reference/colors) of the button when
    it is disabled.
    """

    opacity_on_click: Number = 0.4
    """
    Defines the opacity of the button when it is clicked. When not pressed,
    the button has an opacity of `1.0`.
    """

    min_size: Number = None
    """
    The minimum size of the button.
    """

    size_style: CupertinoButtonSize = CupertinoButtonSize.LARGE
    """
    TBD
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of space to surround the `content` control inside the bounds of the
    button.
    """

    alignment: Optional[Alignment] = None
    """
    TBD
    """

    border_radius: BorderRadiusValue = 8.0
    """
    TBD
    """

    url: Optional[str] = None
    """
    The URL to open when the button is clicked. If registered, `on_click` event is
    fired after that.
    """

    url_target: UrlTarget = UrlTarget.BLANK
    """
    Where to open URL in the web mode.

    Value is of type [`UrlTarget`](https://flet.dev/docs/reference/types/urltarget).
    """

    autofocus: bool = False
    """
    TBD
    """

    focus_color: Optional[ColorValue] = None
    """
    TBD
    """

    on_click: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Fires when a user clicks the button.
    """

    on_long_press: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Fires when a user long-presses the button.
    """

    on_focus: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Fires when the button receives focus.
    """

    on_blur: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Fires when the button loses focus.
    """

    def before_update(self):
        super().before_update()
        assert 0 <= self.opacity_on_click <= 1, (
            "opacity_on_click must be between 0 and 1 inclusive"
        )

    async def focus_async(self):
        await self._invoke_method_async("focus")

    def focus(self):
        asyncio.create_task(self.focus_async())
