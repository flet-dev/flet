from dataclasses import field
from enum import Enum
from typing import Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.duration import Duration, DurationValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ColorValue, Number

__all__ = ["CupertinoTimerPicker", "CupertinoTimerPickerMode"]


class CupertinoTimerPickerMode(Enum):
    HOUR_MINUTE = "hm"
    HOUR_MINUTE_SECONDS = "hms"
    MINUTE_SECONDS = "ms"


@control("CupertinoTimerPicker")
class CupertinoTimerPicker(LayoutControl):
    """
    A countdown timer picker in iOS style.

    It can show a countdown duration with hour, minute and second spinners. The
    duration is bound between `0` and `23` hours `59` minutes `59` seconds.

    ```python
    ft.CupertinoTimerPicker(value=1000)
    ```

    """

    value: DurationValue = field(default_factory=lambda: Duration())
    """
    The initial duration of the countdown timer.

    If specified as an integer, it will be assumed to be in seconds.

    Raises:
        ValueError: If [`value`][(c).] is negative or 24 hours or more.
        ValueError: If [`value`][(c).] is not a multiple
            of [`minute_interval`][(c).] or [`second_interval`][(c).].
    """

    alignment: Alignment = field(default_factory=lambda: Alignment.CENTER)
    """
    Defines how this picker should be positioned within its parent.
    """

    second_interval: int = 1
    """
    The granularity of the second spinner.

    Note:
        Must be a positive integer factor of `60`.

    Raises:
        ValueError: If [`second_interval`][(c).] is not a positive integer factor of
            `60`.
    """

    minute_interval: int = 1
    """
    The granularity of the minute spinner.

    Note:
        Must be a positive integer factor of `60`.

    Raises:
        ValueError: If [`minute_interval`][(c).] is not a positive integer factor of
            `60`.
    """

    mode: CupertinoTimerPickerMode = CupertinoTimerPickerMode.HOUR_MINUTE_SECONDS
    """
    The mode of this picker.
    """

    bgcolor: Optional[ColorValue] = None
    """
    The background color of this picker.
    """

    item_extent: Number = 32.0
    """
    The uniform height of all children.

    Raises:
        ValueError: If [`item_extent`][(c).] is not strictly greater than `0.0`.
    """

    on_change: Optional[ControlEventHandler["CupertinoTimerPicker"]] = None
    """
    Called when the timer's duration changes.

    The [`data`][flet.Event.] property of the event
    handler contains the new duration value.
    Its type matches [`value`][(c).]: if `value` is a `Duration`,
    then `data` is also a `Duration`; otherwise, it is an `int` (seconds).
    """

    def before_update(self):
        super().before_update()
        # normalize for use in below validation checks
        value = (
            self.value
            if isinstance(self.value, Duration)
            else Duration(seconds=self.value)
        )
        if value < Duration():
            raise ValueError("value must be a non-negative duration")
        if value >= Duration(hours=24):
            raise ValueError(
                f"value must be strictly less than 24 hours, got {value.in_hours} hours"
            )
        if not (self.minute_interval > 0 and 60 % self.minute_interval == 0):
            raise ValueError(
                f"minute_interval ({self.minute_interval}) must be a positive "
                "integer factor of 60"
            )
        if not (self.second_interval > 0 and 60 % self.second_interval == 0):
            raise ValueError(
                f"second_interval ({self.second_interval}) must be a positive "
                "integer factor of 60"
            )
        if value.in_minutes % self.minute_interval != 0:
            raise ValueError(
                f"value ({value.in_minutes} minutes) must be a multiple "
                f"of minute_interval ({self.minute_interval})"
            )
        if value.in_seconds % self.second_interval != 0:
            raise ValueError(
                f"value ({value.in_seconds} seconds) must be a multiple "
                f"of second_interval ({self.second_interval})"
            )
        if self.item_extent <= 0:
            raise ValueError(
                f"item_extent must be strictly greater than 0.0, got {self.item_extent}"
            )
