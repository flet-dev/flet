from dataclasses import field
from datetime import datetime, time
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import (
    Event,
    OptionalControlEventHandler,
    OptionalEventHandler,
)
from flet.controls.dialog_control import DialogControl
from flet.controls.types import (
    OptionalColorValue,
    Orientation,
)

__all__ = ["TimePicker", "TimePickerEntryMode", "TimePickerEntryModeChangeEvent"]


class TimePickerEntryMode(Enum):
    DIAL = "dial"
    INPUT = "input"
    DIAL_ONLY = "dialOnly"
    INPUT_ONLY = "inputOnly"


class TimePickerEntryModeChangeEvent(Event["TimePicker"]):
    entry_mode: Optional[TimePickerEntryMode]


@control("TimePicker")
class TimePicker(DialogControl):
    """
    A Material-style time picker dialog.

    Can be opened by calling `page.show_dialog()` method.

    Depending on the `time_picker_entry_mode`, it will show either a Dial or
    an Input (hour and minute text fields) for picking a time.

    Online docs: https://flet.dev/docs/controls/time_picker
    """

    value: Optional[time] = field(default_factory=lambda: datetime.now().time())
    """
    The selected time that the picker should display. The default value is equal
    to the current time.
    """

    modal: bool = False
    """
    TBD
    """

    time_picker_entry_mode: Optional[TimePickerEntryMode] = None
    """
    The initial mode of time entry method for the time picker dialog.

    Value is of type [`TimePickerEntryMode`](https://flet.dev/docs/reference/types/timepickerentrymode)
    and defaults to `TimePickerEntryMode.DIAL`.
    """

    hour_label_text: Optional[str] = None
    """
    The text that is displayed below the hour input text field.

    The default value is "Hour".
    """

    minute_label_text: Optional[str] = None
    """
    The text that is displayed below the minute input text field.

    The default value is "Minute".
    """

    help_text: Optional[str] = None
    """
    The text that is displayed at the top of the header.

    This is used to indicate to the user what they are selecting a time for.
    The default value is "Enter time".
    """

    cancel_text: Optional[str] = None
    """
    The text that is displayed on the cancel button. The default value is "Cancel".
    """

    confirm_text: Optional[str] = None
    """
    The text that is displayed on the confirm button. The default value is "OK".
    """

    error_invalid_text: Optional[str] = None
    """
    The error message displayed below the input text field if the input is not a
    valid hour/minute. The default value is "Enter a valid time".
    """

    orientation: Optional[Orientation] = None
    """
    The orientation of the dialog when displayed. Value is of type `Orientation`
    enum which has the following possible values: `PORTRAIT` and `LANDSCAPE`.
    """

    barrier_color: OptionalColorValue = None
    """
    TBD
    """

    on_change: OptionalControlEventHandler["TimePicker"] = None
    """
    Fires when user clicks confirm button. `value` property is updated with selected
    time. `e.data` also contains the selected time.
    """

    on_entry_mode_change: OptionalEventHandler[TimePickerEntryModeChangeEvent] = None
    """
    Fires when the `time_picker_entry_mode` is changed.

    Event handler argument is of type
    [`TimePickerEntryModeChangeEvent`](https://flet.dev/docs/reference/types/timepickerentrymodechangeevent).
    """
