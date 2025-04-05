from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.border_radius import OptionalBorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import Control, control
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    IconValue,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    UrlTarget,
)

__all__ = ["CupertinoButton"]


@control("CupertinoButton")
class CupertinoButton(ConstrainedControl):
    """
    An iOS-style button.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinobutton
    """

    text: Optional[str] = None
    """Blah blah"""
    icon: Optional[IconValue] = None
    icon_color: OptionalColorValue = None
    content: Optional[Control] = None
    bgcolor: OptionalColorValue = None
    color: OptionalColorValue = None
    disabled_bgcolor: OptionalColorValue = None
    opacity_on_click: Number = 0.4
    min_size: Number = 44.0
    padding: OptionalPaddingValue = None
    alignment: Optional[Alignment] = None
    border_radius: OptionalBorderRadiusValue = None
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
