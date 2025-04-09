from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control import control
from flet.controls.types import Number, OptionalColorValue, OptionalControlEventCallable

__all__ = ["CupertinoTimerPicker", "CupertinoTimerPickerMode"]


class CupertinoTimerPickerMode(Enum):
    HOUR_MINUTE = "hm"
    HOUR_MINUTE_SECONDS = "hms"
    MINUTE_SECONDS = "ms"


@control("CupertinoTimerPicker")
class CupertinoTimerPicker(ConstrainedControl):
    """
    A countdown timer picker in iOS style.

    It can show a countdown duration with hour, minute and second spinners. The duration is bound between 0 and 23 hours 59 minutes 59 seconds.

    -----

    Online docs: https://flet.dev/docs/controls/cupertinotimerpicker
    """

    value: int = 0
    alignment: Optional[Alignment] = None
    second_interval: int = 1
    minute_interval: int = 1
    mode: CupertinoTimerPickerMode = CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS
    bgcolor: OptionalColorValue = None
    item_extent: Number = 32.0
    on_change: OptionalControlEventCallable = None
