from dataclasses import field
from enum import Enum
from typing import Annotated, Optional

from flet.controls.alignment import Alignment
from flet.controls.base_control import control
from flet.controls.control_event import ControlEventHandler
from flet.controls.duration import Duration, DurationValue
from flet.controls.layout_control import LayoutControl
from flet.controls.types import ColorValue, Number
from flet.utils.validation import V

__all__ = ["CupertinoTimerPicker", "CupertinoTimerPickerMode"]


class CupertinoTimerPickerMode(Enum):
    """
    Different modes of :class:`~flet.CupertinoTimerPicker`.
    """

    HOUR_MINUTE = "hm"
    """
    Mode that shows the timer duration in hour and minute.

    Examples: `16 hours | 14 min`
    """

    HOUR_MINUTE_SECONDS = "hms"
    """
    Mode that shows the timer duration in hour, minute, and second.

    Examples: `16 hours | 14 min | 43 sec`
    """

    MINUTE_SECONDS = "ms"
    """
    Mode that shows the timer duration in minute and second.

    Examples: `14 min | 43 sec`
    """


@control("CupertinoTimerPicker")
class CupertinoTimerPicker(LayoutControl):
    """
    A countdown timer picker in iOS style.

    It can show a countdown duration with hour, minute and second spinners. The
    duration is bound between `0` and `23` hours `59` minutes `59` seconds.

    Example:
    ```python
    ft.CupertinoTimerPicker(value=1000)
    ```

    """

    value: DurationValue = field(default_factory=lambda: Duration())
    """
    The initial duration of the countdown timer.

    If specified as an integer, it will be assumed to be in seconds.

    Raises:
        ValueError: If it is not greater than or equal to `0`.
        ValueError: If it is not strictly less than `24` hours.
        ValueError: If it is not a multiple of :attr:`minute_interval`.
        ValueError: If it is not a multiple of :attr:`second_interval`.
    """

    alignment: Alignment = field(default_factory=lambda: Alignment.CENTER)
    """
    Defines how this picker should be positioned within its parent.
    """

    second_interval: Annotated[
        int,
        V.gt(0),
        V.factor_of(60),
    ] = 1
    """
    The granularity of the second spinner.

    Raises:
        ValueError: If it is not strictly greater than `0`.
        ValueError: If it is not a factor of `60`.
    """

    minute_interval: Annotated[
        int,
        V.gt(0),
        V.factor_of(60),
    ] = 1
    """
    The granularity of the minute spinner.

    Raises:
        ValueError: If it is not strictly greater than `0`.
        ValueError: If it is not a factor of `60`.
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
        ValueError: If it is not strictly greater than `0.0`.
    """

    on_change: Optional[ControlEventHandler["CupertinoTimerPicker"]] = None
    """
    Called when the timer's duration changes.

    The :attr:`~flet.Event.data` property of the event
    handler contains the new duration value.
    Its type matches :attr:`value`: if `value` is a `Duration`,
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
        if self.minute_interval > 0 and value.in_minutes % self.minute_interval != 0:
            raise ValueError(
                f"value ({value.in_minutes} minutes) must be a multiple "
                f"of minute_interval ({self.minute_interval})"
            )
        if self.second_interval > 0 and value.in_seconds % self.second_interval != 0:
            raise ValueError(
                f"value ({value.in_seconds} seconds) must be a multiple "
                f"of second_interval ({self.second_interval})"
            )
        if self.item_extent <= 0:
            raise ValueError(
                f"item_extent must be strictly greater than 0.0, got {self.item_extent}"
            )
