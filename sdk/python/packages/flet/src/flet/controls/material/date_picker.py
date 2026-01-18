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
from flet.controls.padding import Padding, PaddingValue
from flet.controls.types import (
    ColorValue,
    IconData,
    Locale,
)

__all__ = [
    "DatePicker",
    "DatePickerEntryMode",
    "DatePickerEntryModeChangeEvent",
    "DatePickerMode",
]


class DatePickerMode(Enum):
    """Initial display of a calendar date picker."""

    DAY = "day"
    """Choosing a month and day."""

    YEAR = "year"
    """Choosing a year."""


class DatePickerEntryMode(Enum):
    """Mode of date entry method for the date picker dialog."""

    CALENDAR = "calendar"
    """
    User picks a date from calendar grid.

    Can switch to [`INPUT`][(c).] by activating a mode button in the dialog.
    """

    INPUT = "input"
    """
    User can input the date by typing it into a text field.

    Can switch to [`CALENDAR`][(c).] by activating a mode button in the dialog.
    """

    CALENDAR_ONLY = "calendarOnly"
    """
    User can only pick a date from calendar grid.

    There is no user interface to switch to another mode.
    """

    INPUT_ONLY = "inputOnly"
    """
    User can only input the date by typing it into a text field.

    There is no user interface to switch to another mode.
    """


@dataclass
class DatePickerEntryModeChangeEvent(Event["DatePicker"]):
    """Event fired when the [`DatePicker`][flet.] entry mode is changed."""

    entry_mode: DatePickerEntryMode
    """The new date picker entry mode."""


@control("DatePicker")
class DatePicker(DialogControl):
    """
    A Material-style date picker dialog.

    It can be opened by calling [`Page.show_dialog()`][flet.Page.show_dialog] method.

    Depending on the [`entry_mode`][(c).], it will show either a Calendar
    or an Input (TextField) for picking a date.
    """

    value: Optional[DateTimeValue] = None
    """
    The selected date that the picker should display.

    Defaults to [`current_date`][(c).].
    """

    modal: bool = False
    """
    Whether this date picker cannot be dismissed by clicking the area outside of it.
    """

    first_date: DateTimeValue = field(
        default_factory=lambda: datetime(year=1900, month=1, day=1)
    )
    """
    The earliest allowable date that the user can select.

    Defaults to `January 1, 1900`.
    """

    last_date: DateTimeValue = field(
        default_factory=lambda: datetime(year=2050, month=1, day=1)
    )
    """
    The latest allowable date that the user can select.

    Defaults to `January 1, 2050`.
    """

    current_date: DateTimeValue = field(default_factory=lambda: datetime.now())
    """
    The date representing today. It will be highlighted in the day grid.
    """

    locale: Optional[Locale] = None
    """
    The locale for this date picker dialog. It is intended for (rare) cases where this
    dialog should be localized differently from the rest of the page.

    It overrides the locale used by the page (see [`Page.locale_configuration`][flet.]),
    but does not participate in page-level locale resolution.

    If set to `None` (the default) or an inexistent/unsupported locale,
    the [`current_locale`][flet.LocaleConfiguration.] of the
    [`Page.locale_configuration`][flet.] is used as fallback.
    """

    keyboard_type: KeyboardType = KeyboardType.DATETIME
    """
    The type of keyboard to use for editing the text.
    """

    date_picker_mode: DatePickerMode = DatePickerMode.DAY
    """
    Initial display mode of this picker.
    """

    entry_mode: DatePickerEntryMode = DatePickerEntryMode.CALENDAR
    """
    The initial mode of date entry method for the date picker dialog.
    """

    help_text: Optional[str] = None
    """
    The text that is displayed at the top of the header.

    This is used to indicate to the user what they are selecting a date for.

    Defaults to `"Select date"`.
    """

    cancel_text: Optional[str] = None
    """
    The text that is displayed on the cancel button.

    Defaults to `"Cancel"`.
    """

    confirm_text: Optional[str] = None
    """
    The text that is displayed on the confirm button.

    Defaults to `"OK"`.
    """

    error_format_text: Optional[str] = None
    """
    The error message displayed below the text field if the entered date is not in the
    correct format.

    Defaults to `"Invalid format"`.
    """

    error_invalid_text: Optional[str] = None
    """
    The error message displayed below the text field if the date is earlier than
    [`first_date`][(c).] or later than [`last_date`][(c).].

    Defaults to `"Out of range"`.
    """

    field_hint_text: Optional[str] = None
    """
    The hint text displayed in the text field.

    The default value is the date format string that depends on your locale.
    For example, `'mm/dd/yyyy'` for en_US.
    """

    field_label_text: Optional[str] = None
    """
    The label text displayed in the `TextField`.

    If `None`, defaults to the words representing the date format string.
    For example, `'Month, Day, Year'` for en_US.

    Defaults to `"Enter Date"`.
    """

    switch_to_calendar_icon: Optional[IconData] = None
    """
    The icon displayed in the corner of this picker's dialog when
    [`entry_mode`][(c).] is [`DatePickerEntryMode.INPUT`][flet.].

    Clicking on this icon changes the [`entry_mode`][(c).] to
    [`DatePickerEntryMode.CALENDAR`][flet.].

    If `None`, defaults to [`Icons.CALENDAR_TODAY`][flet.].
    """

    switch_to_input_icon: Optional[IconData] = None
    """
    The icon displayed in the corner of this picker's dialog when
    [`entry_mode`][(c).] is [`DatePickerEntryMode.CALENDAR`][flet.].

    Clicking on icon changes the [`entry_mode`][(c).] to
    [`DatePickerEntryMode.INPUT`][flet.].

    If `None`, defaults to [`Icons.EDIT_OUTLINED`][flet.].
    """

    barrier_color: Optional[ColorValue] = None
    """
    The color of the modal barrier that darkens everything below this picker's dialog.

    If `None`, the [`DialogTheme.barrier_color`][flet.] is used.
    If it is also `None`, then [`Colors.BLACK_54`][flet.] is used.
    """

    inset_padding: PaddingValue = field(
        default_factory=lambda: Padding.symmetric(horizontal=16.0, vertical=24.0)
    )
    """
    The amount of padding added to [`view_insets`][flet.PageMediaData.] of the
    [`Page.media`][flet.] on the outside of this picker's dialog.

    This defines the minimum space between the screen's edges and the dialog.
    """

    on_change: Optional[ControlEventHandler["DatePicker"]] = None
    """
    Called when user clicks confirm button.
    [`value`][(c).] is updated with selected date.

    The [`data`][flet.Event.] property of the event handler argument
    contains the selected date.
    """

    on_entry_mode_change: Optional[EventHandler[DatePickerEntryModeChangeEvent]] = None
    """
    Called when the [`entry_mode`][(c).] is changed from the user interface.
    """
