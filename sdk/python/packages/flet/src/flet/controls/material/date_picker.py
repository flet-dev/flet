from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import ControlEvent
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import DateTimeValue
from flet.controls.material.textfield import KeyboardType
from flet.controls.types import (
    IconValue,
    OptionalColorValue,
    OptionalControlEventCallable,
    OptionalEventCallable,
)

__all__ = [
    "DatePicker",
    "DatePickerMode",
    "DatePickerEntryMode",
    "DatePickerEntryModeChangeEvent",
]


class DatePickerMode(Enum):
    DAY = "day"
    YEAR = "year"


class DatePickerEntryMode(Enum):
    CALENDAR = "calendar"
    INPUT = "input"
    CALENDAR_ONLY = "calendarOnly"
    INPUT_ONLY = "inputOnly"


@dataclass
class DatePickerEntryModeChangeEvent(ControlEvent):
    entry_mode: Optional[DatePickerEntryMode]


@control("DatePicker")
class DatePicker(DialogControl):
    """
    A Material-style date picker dialog.

    It is added to [`page.overlay`](page#overlay) and can be opened by setting `open=True` or by calling `Page.open()` method.

    Depending on the `date_picker_entry_mode`, it will show either a Calendar or an Input (TextField) for picking a date.

    Online docs: https://flet.dev/docs/controls/datepicker
    """

    value: Optional[DateTimeValue] = None
    modal: bool = False
    first_date: DateTimeValue = field(
        default_factory=lambda: datetime(year=1900, month=1, day=1)
    )
    last_date: DateTimeValue = field(
        default_factory=lambda: datetime(year=2050, month=1, day=1)
    )
    current_date: DateTimeValue = field(default_factory=lambda: datetime.now())
    keyboard_type: KeyboardType = KeyboardType.DATETIME
    date_picker_mode: DatePickerMode = DatePickerMode.DAY
    date_picker_entry_mode: DatePickerEntryMode = DatePickerEntryMode.CALENDAR
    help_text: Optional[str] = None
    cancel_text: Optional[str] = None
    confirm_text: Optional[str] = None
    error_format_text: Optional[str] = None
    error_invalid_text: Optional[str] = None
    field_hint_text: Optional[str] = None
    field_label_text: Optional[str] = None
    switch_to_calendar_icon: Optional[IconValue] = None
    switch_to_input_icon: Optional[IconValue] = None
    barrier_color: OptionalColorValue = None
    on_change: OptionalControlEventCallable = None
    on_entry_mode_change: OptionalEventCallable[DatePickerEntryModeChangeEvent] = None
