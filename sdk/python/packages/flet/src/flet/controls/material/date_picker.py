from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import (
    ControlEventHandler,
    Event,
    EventHandler,
)
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import DateTimeValue
from flet.controls.material.textfield import KeyboardType
from flet.controls.types import (
    ColorValue,
    IconValue,
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
class DatePickerEntryModeChangeEvent(Event["DatePicker"]):
    entry_mode: Optional[DatePickerEntryMode]


@control("DatePicker")
class DatePicker(DialogControl):
    """
    A Material-style date picker dialog.

    It is added to [`Page.overlay`][(p).] and can be opened by
    calling [`Page.open_dialog()`][flet.Page.open_dialog] method.

    Depending on the `date_picker_entry_mode`, it will show either a Calendar or an
    Input (TextField) for picking a date.
    """

    value: Optional[DateTimeValue] = None
    """
    The selected date that the picker should display.

    Defaults to [`current_date`][flet.DatePicker.current_date].
    """

    modal: bool = False
    """
    Whether this date picker cannot be dismissed by clicking the area outside of it.
    """

    first_date: DateTimeValue = field(
        default_factory=lambda: datetime(year=1900, month=1, day=1)
    )
    """
    The earliest allowable date that the user can select. Defaults to `January 1, 1900`.
    """

    last_date: DateTimeValue = field(
        default_factory=lambda: datetime(year=2050, month=1, day=1)
    )
    """
    The latest allowable date that the user can select. Defaults to `January 1, 2050`.
    """

    current_date: DateTimeValue = field(default_factory=lambda: datetime.now())
    """
    The date representing today. It will be highlighted in the day grid.
    """

    keyboard_type: KeyboardType = KeyboardType.DATETIME
    """
    The type of keyboard to use for editing the text.

    Type: [`KeyboardType`][flet.KeyboardType]
    and defaults to `KeyboardType.DATETIME`.
    """

    date_picker_mode: DatePickerMode = DatePickerMode.DAY
    """
    Initial display of a calendar date picker.

    Type: [`DatePickerMode`][flet.DatePickerMode]
    and defaults to `DatePickerMode.DAY`.
    """

    date_picker_entry_mode: DatePickerEntryMode = DatePickerEntryMode.CALENDAR
    """
    The initial mode of date entry method for the date picker dialog.

    Type: [`DatePickerEntryMode`][flet.DatePickerEntryMode]
    and defaults to `DatePickerEntryMode.CALENDAR`.
    """

    help_text: Optional[str] = None
    """
    The text that is displayed at the top of the header.

    This is used to indicate to the user what they are selecting a date for.

    Defaults to `"Select date"`.
    """

    cancel_text: Optional[str] = None
    """
    The text that is displayed on the cancel button. Defaults to `"Cancel"`.
    """

    confirm_text: Optional[str] = None
    """
    The text that is displayed on the confirm button. Defaults to `"OK"`.
    """

    error_format_text: Optional[str] = None
    """
    The error message displayed below the TextField if the entered date is not in the
    correct format.

    Defaults to `"Invalid format"`.
    """

    error_invalid_text: Optional[str] = None
    """
    The error message displayed below the TextField if the date is earlier than
    `first_date` or later than `last_date`.

    Defaults to `"Out of range"`.
    """

    field_hint_text: Optional[str] = None
    """
    The hint text displayed in the text field.

    The default value is the date format string that depends on your locale. For
    example, 'mm/dd/yyyy' for en_US.
    """

    field_label_text: Optional[str] = None
    """
    The label text displayed in the TextField.

    Defaults to `"Enter Date"`.
    """

    switch_to_calendar_icon: Optional[IconValue] = None
    """
    Name of the icon displayed in the corner of the dialog when `DatePickerEntryMode`
    is `DatePickerEntryMode.INPUT`.
    Clicking on icon changes the `DatePickerEntryMode` to
    `DatePickerEntryMode.CALENDAR`. If `None`, `icons.CALENDAR_TODAY` is used.
    """

    switch_to_input_icon: Optional[IconValue] = None
    """
    Name of the icon displayed in the corner of the dialog when `DatePickerEntryMode`
    is `DatePickerEntryMode.CALENDAR`.
    Clicking on icon changes the `DatePickerEntryMode` to `DatePickerEntryMode.INPUT`.
    If `None`, `icons.EDIT_OUTLINED` is used.
    """

    barrier_color: Optional[ColorValue] = None
    """
    The [color](https://flet.dev/docs/reference/colors) of the modal barrier that
    darkens everything below the date picker.

    If `None`, the [`DialogTheme.barrier_color`](https://flet.dev/docs/reference/types/dialogtheme#barrier_color)
    is used.
    If it is also `None`, then `Colors.BLACK_54` is used.
    """

    on_change: Optional[ControlEventHandler["DatePicker"]] = None
    """
    Called when user clicks confirm button. `value` property is updated with selected
    date. `e.data` also contains the selected date.
    """

    on_entry_mode_change: Optional[EventHandler[DatePickerEntryModeChangeEvent]] = None
    """
    Called when the `date_picker_entry_mode` is changed.

    Event handler argument is of
    type [`DatePickerEntryModeChangeEvent`][flet.DatePickerEntryModeChangeEvent]
    """
