from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadius, BorderRadiusValue
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.geometry import Size
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    IconValueOrControl,
    MouseCursor,
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

    Raises:
        AssertionError: If [`opacity_on_click`][(c).] is not between `0.0`
            and `1.0` inclusive.
    """

    content: Optional[StrOrControl] = None
    """
    The content of the button. Can be either a string or a control.
    """

    icon: Optional[IconValueOrControl] = None
    """
    Icon shown in the button.
    """

    icon_color: Optional[ColorValue] = None
    """
    Icon color.
    """

    bgcolor: Optional[ColorValue] = None
    """
    Button's background color.
    """

    color: Optional[ColorValue] = None
    """
    Button's text color.
    """

    disabled_bgcolor: Optional[ColorValue] = None
    """
    The background color of the button when
    it is disabled.
    """

    opacity_on_click: Number = 0.4
    """
    Defines the opacity of the button when it is clicked.

    When not pressed, the button has an opacity of `1.0`.
    """

    min_size: Optional[Size] = None
    """
    The minimum size of this button.
    """

    size: CupertinoButtonSize = CupertinoButtonSize.LARGE
    """
    The size of this button.
    """

    padding: Optional[PaddingValue] = None
    """
    The amount of space to surround the `content` control inside the bounds of the
    button.
    """

    alignment: Optional[Alignment] = field(default_factory=lambda: Alignment.CENTER)
    """
    The alignment of the button's child.

    Typically buttons are sized to be just big enough to contain the child
    and its padding. If the button's size is constrained to a fixed size,
    this property defines how the child is aligned within the available space.
    """

    border_radius: BorderRadiusValue = field(
        default_factory=lambda: BorderRadius.all(8.0)
    )
    """
    The radius of the button's corners when it has a background color.
    """

    url: Optional[str] = None
    """
    The URL to open when the button is clicked. If registered, `on_click` event is
    fired after that.
    """

    url_target: UrlTarget = UrlTarget.BLANK
    """
    Where to open URL in the web mode.
    """

    autofocus: bool = False
    """
    Whether this button should be selected as the initial focus when no other
    node in its scope is currently focused.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color to use for the focus highlight for keyboard interactions.

    Defaults to a slightly transparent [`bgcolor`][flet.CupertinoButton.bgcolor].
    If `bgcolor` is `None`, defaults to a slightly transparent
    [`CupertinoColors.ACTIVE_BLUE`][flet.CupertinoColors.ACTIVE_BLUE].
    'Slightly transparent' in this context means the color is used with an opacity
    of `0.80`, a brightness of `0.69` and a saturation of `0.835`.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer when it enters or is hovering over this button.
    """

    on_click: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Called when a user clicks the button.
    """

    on_long_press: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Called when a user long-presses the button.
    """

    on_focus: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Called when the button receives focus.
    """

    on_blur: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Called when the button loses focus.
    """

    def before_update(self):
        super().before_update()
        assert 0 <= self.opacity_on_click <= 1, (
            "opacity_on_click must be between 0 and 1 inclusive, "
            f"got {self.opacity_on_click}"
        )

    async def focus(self):
        await self._invoke_method("focus")
