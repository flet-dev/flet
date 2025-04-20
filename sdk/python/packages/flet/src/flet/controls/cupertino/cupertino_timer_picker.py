from dataclasses import field
from enum import Enum

from flet.controls import alignment
from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.duration import Duration, DurationValue
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

    value: DurationValue = field(default_factory=lambda: Duration())
    alignment: Alignment = field(default_factory=lambda: alignment.center)
    second_interval: int = 1
    minute_interval: int = 1
    mode: CupertinoTimerPickerMode = CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS
    bgcolor: OptionalColorValue = None
    item_extent: Number = 32.0
    on_change: OptionalControlEventCallable = None

    def before_update(self):
        super().before_update()
        value = (
            self.value
            if isinstance(self.value, Duration)
            else Duration(seconds=self.value)
        )
        assert value >= Duration(), "value must be a non-negative duration"
        assert value < Duration(hours=24), "value must be strictly less than 24 hours"
        assert (
            self.minute_interval > 0 and 60 % self.minute_interval == 0
        ), f"minute_interval ({self.minute_interval}) must be a positive integer factor of 60"
        assert (
            self.second_interval > 0 and 60 % self.second_interval == 0
        ), f"second_interval ({self.second_interval}) must be a positive integer factor of 60"
        assert (
            value.in_minutes % self.minute_interval == 0
        ), f"value ({value.in_minutes} minutes) must be a multiple of minute_interval ({self.minute_interval})"
        assert (
            value.in_seconds % self.second_interval == 0
        ), f"value ({value.in_seconds} seconds) must be a multiple of second_interval ({self.second_interval})"
        assert self.item_extent > 0, "item_extent must be strictly greater than 0"
