from dataclasses import field
from enum import Enum
from typing import Optional

from flet.core.alignment import Alignment
from flet.core.constrained_control import ConstrainedControl
from flet.core.control import control
from flet.core.types import ColorValue, Number, OptionalControlEventCallable

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

    value: int = field(default=0)
    alignment: Optional[Alignment] = None
    second_interval: int = field(default=1)
    minute_interval: int = field(default=1)
    mode: Optional[CupertinoTimerPickerMode] = None
    bgcolor: Optional[ColorValue] = None
    item_extent: Number = field(default=32.0)
    on_change: OptionalControlEventCallable = None
