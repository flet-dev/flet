from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.buttons import OutlinedBorder
from flet.controls.control import Control
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import OptionalDurationValue
from flet.controls.margin import OptionalMarginValue
from flet.controls.padding import OptionalPaddingValue
from flet.controls.types import (
    ClipBehavior,
    Number,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalNumber,
)

__all__ = ["SnackBar", "SnackBarBehavior", "DismissDirection"]


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
class SnackBar(DialogControl):
    """
    A lightweight message with an optional action which briefly displays at the bottom
    of the screen.

    Online docs: https://flet.dev/docs/controls/snackbar
    """

    content: Control
    behavior: Optional[SnackBarBehavior] = None
    dismiss_direction: Optional[DismissDirection] = None
    show_close_icon: bool = False
    action: Optional[str] = None
    action_color: OptionalColorValue = None
    close_icon_color: OptionalColorValue = None
    bgcolor: OptionalColorValue = None
    duration: OptionalDurationValue = None
    margin: OptionalMarginValue = None
    padding: OptionalPaddingValue = None
    width: OptionalNumber = None
    elevation: OptionalNumber = None
    shape: Optional[OutlinedBorder] = None
    clip_behavior: Optional[ClipBehavior] = None
    action_overflow_threshold: Number = 0.25
    on_action: OptionalControlEventCallable = None
    on_visible: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        assert (
            self.action_overflow_threshold is None
            or 0 <= self.action_overflow_threshold <= 1
        ), "action_overflow_threshold must be between 0 and 1 inclusive"
        assert (
            self.elevation is None or self.elevation >= 0
        ), "elevation cannot be negative"
