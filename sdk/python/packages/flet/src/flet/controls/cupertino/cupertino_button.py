from dataclasses import field
from enum import Enum
from typing import Optional, Union

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.border_radius import BorderRadius, BorderRadiusValue
from flet.controls.control_event import ControlEventHandler
from flet.controls.geometry import Size
from flet.controls.layout_control import LayoutControl
from flet.controls.padding import PaddingValue
from flet.controls.types import (
    ColorValue,
    IconDataOrControl,
    MouseCursor,
    Number,
    StrOrControl,
    Url,
)

__all__ = ["CupertinoButton", "CupertinoButtonSize"]


class CupertinoButtonSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@control("CupertinoButton")
class CupertinoButton(LayoutControl):
    """
    An iOS-style button.

    ```python
    ft.CupertinoButton("Tap me")
    ```
    """

    content: Optional[StrOrControl] = None
    """
    The content of this button.
    """

    icon: Optional[IconDataOrControl] = None
    """
    An icon shown in this button.
    """

    icon_color: Optional[ColorValue] = None
    """
    The foreground color of the [`icon`][(c).].
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this button.
    """

    color: Optional[ColorValue] = None
    """
    The color of this button's text.
    """

    disabled_bgcolor: Optional[ColorValue] = None
    """
    The background color of this button when disabled.
    """

    opacity_on_click: Number = 0.4
    """
    Defines the opacity of the button when it is clicked.

    When not pressed, the button has an opacity of `1.0`.

    Raises:
        ValueError: If [`opacity_on_click`][(c).] is not between `0.0`
            and `1.0` inclusive.
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
    The alignment of this button's content.

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

    url: Optional[Union[str, Url]] = None
    """
    The URL to open when this button is clicked.

    Additionally, if [`on_click`][(c).] event callback is
    provided, it is fired after that.
    """

    autofocus: bool = False
    """
    Whether this button should be selected as the initial focus when no other
    node in its scope is currently focused.
    """

    focus_color: Optional[ColorValue] = None
    """
    The color to use for the focus highlight for keyboard interactions.

    Defaults to a slightly transparent [`bgcolor`][(c).].
    If `bgcolor` is `None`, defaults to a slightly transparent
    [`CupertinoColors.ACTIVE_BLUE`][flet.].
    'Slightly transparent' in this context means the color is used with an opacity
    of `0.80`, a brightness of `0.69` and a saturation of `0.835`.
    """

    mouse_cursor: Optional[MouseCursor] = None
    """
    The cursor for a mouse pointer when it enters or is hovering over this button.
    """

    on_click: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Called when a user clicks this button.
    """

    on_long_press: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Called when a user long-presses this button.
    """

    on_focus: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Called when this button receives focus.
    """

    on_blur: Optional[ControlEventHandler["CupertinoButton"]] = None
    """
    Called when this button loses focus.
    """

    def before_update(self):
        super().before_update()
        if not (0 <= self.opacity_on_click <= 1):
            raise ValueError(
                "opacity_on_click must be between 0 and 1 inclusive, "
                f"got {self.opacity_on_click}"
            )

    async def focus(self):
        await self._invoke_method("focus")
