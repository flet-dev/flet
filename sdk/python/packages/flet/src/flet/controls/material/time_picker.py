from dataclasses import field
from datetime import datetime, time
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEvent
from flet.controls.dialog_control import DialogControl
from flet.controls.types import (
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
    Orientation,
)

__all__ = ["TimePicker", "TimePickerEntryMode", "TimePickerEntryModeChangeEvent"]


class TimePickerEntryMode(Enum):
    DIAL = "dial"
    INPUT = "input"
    DIAL_ONLY = "dialOnly"
    INPUT_ONLY = "inputOnly"


class TimePickerEntryModeChangeEvent(ControlEvent):
    entry_mode: Optional[TimePickerEntryMode]


@control("TimePicker")
class TimePicker(DialogControl):
    """
    A Material-style time picker dialog.

    Can be opened by calling `page.show_dialog()` method.

    Depending on the `time_picker_entry_mode`, it will show either a Dial or an Input
    (hour and minute text fields) for picking a time.

    Online docs: https://flet.dev/docs/controls/time_picker
    """

    value: Optional[time] = field(default_factory=lambda: datetime.now().time())
    modal: bool = False
    time_picker_entry_mode: Optional[TimePickerEntryMode] = None
    hour_label_text: Optional[str] = None
    minute_label_text: Optional[str] = None
    help_text: Optional[str] = None
    cancel_text: Optional[str] = None
    confirm_text: Optional[str] = None
    error_invalid_text: Optional[str] = None
    orientation: Optional[Orientation] = None
    barrier_color: OptionalColorValue = None
    on_change: OptionalControlEventCallable = None
    on_entry_mode_change: OptionalEventCallable[TimePickerEntryModeChangeEvent] = None
