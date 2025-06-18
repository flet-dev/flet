from dataclasses import field
from enum import Enum
from typing import Optional, Union

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.control_event import OptionalControlEventHandler
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import Duration, DurationValue
from flet.controls.margin import OptionalMarginValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    ClipBehavior,
    Number,
    OptionalColorValue,
    OptionalNumber,
    StrOrControl,
)

__all__ = ["SnackBar", "SnackBarBehavior", "DismissDirection", "SnackBarAction"]


class SnackBarBehavior(Enum):
    FIXED = "fixed"
    FLOATING = "floating"


class DismissDirection(Enum):
    NONE = "none"
    VERTICAL = "vertical"
    HORIZONTAL = "horizontal"
    END_TO_START = "endToStart"
    START_TO_END = "startToEnd"
    UP = "up"
    DOWN = "down"


@control("SnackBar")
class SnackBarAction(Control):
    """A button that can be used as an action in a `SnackBar`."""

    label: str
    """
    The button's label.
    """

    text_color: OptionalColorValue = None
    """
    The button label color.
    If not provided, defaults to `SnackBarTheme.action_text_color`.
    """

    disabled_text_color: OptionalColorValue = None
    """
    The button disabled label color. 
    This color is shown after the action is dismissed.
    """

    bgcolor: OptionalColorValue = None
    """
    The button background fill color. 
    If not provided, defaults to `SnackBarTheme.action_bgcolor`.
    """

    disabled_bgcolor: OptionalColorValue = None
    """
    The button disabled background color. 
    This color is shown after the action is dismissed.
    
    If not provided, defaults to `SnackBarTheme.disabled_action_bgcolor`.
    """

    on_click: OptionalControlEventHandler["SnackBarAction"] = None
    """
    Fires when this action button is clicked.
    """


@control("SnackBar")
class SnackBar(DialogControl):
    """
    A lightweight message with an optional action which briefly displays at the
    bottom of the screen.

    Online docs: https://flet.dev/docs/controls/snackbar
    """

    content: StrOrControl
    """
    The primary content of the snack bar.

    Typically a [`Text`](https://flet.dev/docs/controls/text) control.
    """

    behavior: Optional[SnackBarBehavior] = None
    """
    This defines the behavior and location of the snack bar.

    Defines where a SnackBar should appear within a page and how its location
    should be adjusted when the page also includes a `FloatingActionButton` or a
    `NavigationBar`.

    Value is of type
    [`SnackBarBehavior`](https://flet.dev/docs/reference/types/snackbarbehavior)
    and defaults to `SnackBarBehavior.FIXED`.

    **Note:**

    * If `behavior=SnackBarBehavior.FLOATING`, the length of the bar is defined
      by either `width` or `margin`, and if both are specified, `width` takes
      precedence over `margin`.
    * `width` and `margin` are ignored if `behavior!=SnackBarBehavior.FLOATING`.
    """

    dismiss_direction: Optional[DismissDirection] = None
    """
    The direction in which the SnackBar can be dismissed.

    Value is of type
    [`DismissDirection`](https://flet.dev/docs/reference/types/dismissdirection)
    and defaults to `DismissDirection.DOWN`.
    """

    show_close_icon: bool = False
    """
    Whether to include a "close" icon widget.

    Tapping the icon will close the snack bar.
    """

    action: Union[str, SnackBarAction, None] = None
    """
    An optional action that the user can take based on the snack bar.

    For example, the snack bar might let the user undo the operation that prompted
    the snackbar. Snack bars can have at most one action.

    The action should not be "dismiss" or "cancel".
    """

    close_icon_color: OptionalColorValue = None
    """
    An optional color for the close icon, if `show_close_icon=True`.
    """

    bgcolor: OptionalColorValue = None
    """
    SnackBar background [color](https://flet.dev/docs/reference/colors).
    """

    duration: DurationValue = field(default_factory=lambda: Duration(milliseconds=4000))
    """
    The number of *milliseconds* that the SnackBar stays open for.

    Defaults to `4000`
    ([4 seconds](https://api.flutter.dev/flutter/material/SnackBar/duration.html)).
    """

    margin: OptionalMarginValue = None
    """
    Empty space to surround the snack bar.

    Has effect only when `behavior=SnackBarBehavior.FLOATING` and will be ignored
    if `width` is specified.
    """

    padding: OptionalPaddingValue = None
    """
    The amount of padding to apply to the snack bar's content and optional action.

    Value is of type
    [`Padding`](https://flet.dev/docs/reference/types/padding) or a number.
    """

    width: OptionalNumber = None
    """
    The width of the snack bar.

    If width is specified, the snack bar will be centered horizontally in the
    available space.

    Has effect only when `behavior=SnackBarBehavior.FLOATING`. It can not be used
    if `margin` is specified.
    """

    elevation: OptionalNumber = None
    """
    The z-coordinate at which to place the snack bar. This controls the size of the
    shadow below the snack bar.
    """

    shape: Optional[OutlinedBorder] = None
    """
    The shape of the snack bar's.

    Value is of type
    [`OutlinedBorder`](https://flet.dev/docs/reference/types/outlinedborder).
    """

    clip_behavior: ClipBehavior = ClipBehavior.HARD_EDGE
    """
    The `content` will be clipped (or not) according to this option.

    Value is of type
    [`ClipBehavior`](https://flet.dev/docs/reference/types/clipbehavior) and
    defaults to `ClipBehavior.HARD_EDGE`.
    """

    action_overflow_threshold: Number = 0.25
    """
    The percentage (between `0.0` and `1.0`) threshold for `action`'s width before
    it overflows to a new line.

    If the width of the snackbar's `content` is greater than this percentage of the
    width of the snackbar minus the width of its `action`, then the `action` will
    appear below the `content`.

    At a value of `0.0`, the `action` will not overflow to a new line.

    Defaults to `0.25`.
    """

    on_action: OptionalControlEventHandler["SnackBar"] = None
    """
    Fires when action button is clicked.
    """

    on_visible: OptionalControlEventHandler["SnackBar"] = None
    """
    Fires the first time that the snackbar is visible within the page.
    """

    def before_update(self):
        super().before_update()
        assert isinstance(self.content, str) or (
            isinstance(self.content, Control) and self.content.visible
        ), "content must be a string or a visible control"
        assert (
            self.action_overflow_threshold is None
            or 0 <= self.action_overflow_threshold <= 1
        ), "action_overflow_threshold must be between 0 and 1 inclusive"
        assert self.elevation is None or self.elevation >= 0, (
            "elevation cannot be negative"
        )
