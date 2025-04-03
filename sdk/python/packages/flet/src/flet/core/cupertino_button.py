from dataclasses import field
from typing import Optional

from flet.core.alignment import Alignment
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import Control, control
from flet.core.types import (
    BorderRadiusValue,
    ColorValue,
    IconValue,
    Number,
    OptionalControlEventCallable,
    PaddingValue,
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
    icon_color: Optional[ColorValue] = None
    content: Optional[Control] = None
    bgcolor: Optional[ColorValue] = None
    color: Optional[ColorValue] = None
    disabled_bgcolor: Optional[ColorValue] = None
    opacity_on_click: Number = 0.4
    min_size: Number = 44.0
    padding: Optional[PaddingValue] = None
    alignment: Optional[Alignment] = None
    border_radius: Optional[BorderRadiusValue] = None
    url: Optional[str] = None
    url_target: Optional[UrlTarget] = None
    on_click: OptionalControlEventCallable = None
    on_long_press: OptionalControlEventCallable = None
    on_focus: OptionalControlEventCallable = None
    on_blur: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            0 <= self.opacity_on_click <= 1
        ), "opacity_on_click must be between 0 and 1 inclusive"
