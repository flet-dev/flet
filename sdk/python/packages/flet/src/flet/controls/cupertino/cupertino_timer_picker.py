from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.constrained_control import ConstrainedControl
from flet.controls.control_event import ControlEventHandler
from flet.controls.duration import Duration, DurationValue
from flet.controls.types import ColorValue, Number

__all__ = ["CupertinoTimerPicker", "CupertinoTimerPickerMode"]


class CupertinoTimerPickerMode(Enum):
    HOUR_MINUTE = "hm"
    HOUR_MINUTE_SECONDS = "hms"
    MINUTE_SECONDS = "ms"


@control("CupertinoTimerPicker")
class CupertinoTimerPicker(ConstrainedControl):
    """
    A countdown timer picker in iOS style.

    It can show a countdown duration with hour, minute and second spinners. The
    duration is bound between 0 and 23 hours 59 minutes 59 seconds.

    Raises:
        AssertionError: If [`value`][(c).] is negative.
        AssertionError: If [`value`][(c).] is 24 hours or more.
        AssertionError: If [`minute_interval`][(c).] is not a positive integer factor of `60`.
        AssertionError: If [`second_interval`][(c).] is not a positive integer factor of `60`.
        AssertionError: If [`value`][(c).] is not a multiple of [`minute_interval`][(c).].
        AssertionError: If [`value`][(c).] is not a multiple of [`second_interval`][(c).].
        AssertionError: If [`item_extent`][(c).] is not strictly greater than `0.0`.
    """

    value: DurationValue = field(default_factory=lambda: Duration())
    """
    The initial duration in seconds of the countdown timer.
    """

    alignment: Alignment = field(default_factory=lambda: Alignment.CENTER)
    """
    Defines how the timer picker should be positioned within its parent.
    """

    second_interval: int = 1
    """
    The granularity of the second spinner.

    Note:
        Must be a positive integer factor of `60`.
    """

    minute_interval: int = 1
    """
    The granularity of the minute spinner.

    Note:
        Must be a positive integer factor of `60`.
    """

    mode: CupertinoTimerPickerMode = CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS
    """
    The mode of the timer picker.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this timer picker.
    """

    item_extent: Number = 32.0
    """
    The uniform height of all children.
    """

    on_change: Optional[ControlEventHandler["CupertinoTimerPicker"]] = None
    """
    Called when the timer's duration changes.
    
    The [`data`][flet.Event] property of the event handler argument is the new duration.
    It has the same [type][flet.DurationValue] as [`value`][flet.CupertinoTimerPicker.value].
    """

    def before_update(self):
        super().before_update()
        # normalize for use in below assertion checks
        value = (
            self.value
            if isinstance(self.value, Duration)
            else Duration(seconds=self.value)
        )
        assert value >= Duration(), "value must be a non-negative duration"
        assert value < Duration(
            hours=24
        ), f"value must be strictly less than 24 hours, got {value.in_hours} hours"
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
        assert (
            self.item_extent > 0
        ), f"item_extent must be strictly greater than 0.0, got {self.item_extent}"
