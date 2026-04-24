from dataclasses import field
from datetime import datetime
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import (
    ControlEventHandler,
)
from flet.controls.dialog_control import DialogControl
from flet.controls.duration import DateTimeValue
from flet.controls.material.date_picker import DatePickerEntryMode
from flet.controls.material.textfield import KeyboardType
from flet.controls.types import (
    ColorValue,
    IconData,
    Locale,
)

__all__ = [
    "DateRangePicker",
]


@control("DateRangePicker")
class DateRangePicker(DialogControl):
    """
    A Material-style date range picker dialog.

    It can be opened by calling :meth:`flet.Page.show_dialog` method.

    Depending on the :attr:`entry_mode`, it will show either a Calendar
    or an Input (text field) for picking a date range.

    ```python
    picker = ft.DateRangePicker()

    ft.Button(
        "Pick date range",
        icon=ft.Icons.DATE_RANGE,
        on_click=lambda _: page.show_dialog(picker),
    )
    ```
    """

    start_value: Optional[DateTimeValue] = None
    """
    The selected start date that the picker should display.

    Defaults to :attr:`current_date`.
    """

    end_value: Optional[DateTimeValue] = None
    """
    The selected end date that the picker should display.

    Defaults to :attr:`current_date`.
    """

    save_text: Optional[str] = None
    """
    The label on the save button for the fullscreen calendar mode.
    """

    error_invalid_range_text: Optional[str] = None
    """
    The message used when the date range is invalid (e.g. start date is after end \
    date).
    """

    modal: bool = False
    """
    Whether this date picker cannot be dismissed by clicking the area outside of it.
    """

    first_date: DateTimeValue = field(
        default_factory=lambda: datetime(year=1900, month=1, day=1)
    )
    """
    The earliest allowable date on the date range.
    """

    last_date: DateTimeValue = field(
        default_factory=lambda: datetime(year=2050, month=1, day=1)
    )
    """
    The latest allowable date on the date range.
    """

    current_date: DateTimeValue = field(default_factory=lambda: datetime.now())
    """
    The date representing today. It will be highlighted in the day grid.
    """

    locale: Optional[Locale] = None
    """
    The locale for this date picker dialog. It is intended for (rare) cases where this \
    dialog should be localized differently from the rest of the page.

    It overrides the locale used by the page (see \
    :attr:`flet.Page.locale_configuration`),
    but does not participate in page-level locale resolution.

    If set to `None` (the default) or an inexistent/unsupported locale,
    the :attr:`~flet.LocaleConfiguration.current_locale` of the
    :attr:`flet.Page.locale_configuration` is used as fallback.
    """

    keyboard_type: KeyboardType = KeyboardType.DATETIME
    """
    The type of keyboard to use for editing the text.
    """

    entry_mode: DatePickerEntryMode = DatePickerEntryMode.CALENDAR
    """
    The initial mode of date entry method for the date picker dialog.
    """

    help_text: Optional[str] = None
    """
    The text that is displayed at the top of the header.

    This is used to indicate to the user what they are selecting a date for.
    """

    cancel_text: Optional[str] = None
    """
    The text that is displayed on the cancel button.
    """

    confirm_text: Optional[str] = None
    """
    The text that is displayed on the confirm button.
    """

    error_format_text: Optional[str] = None
    """
    The error message displayed below the TextField if the entered date is not in the \
    correct format.
    """

    error_invalid_text: Optional[str] = None
    """
    The error message displayed below the TextField if the date is earlier than \
    :attr:`first_date` or later than :attr:`last_date`.
    """

    field_start_hint_text: Optional[str] = None
    """
    The text used to prompt the user when no text has been entered in the start field.
    """

    field_end_hint_text: Optional[str] = None
    """
    The text used to prompt the user when no text has been entered in the end field.
    """

    field_start_label_text: Optional[str] = None
    """
    The label for the start date text input field.
    """

    field_end_label_text: Optional[str] = None
    """
    The label for the end date text input field.
    """

    switch_to_calendar_icon: Optional[IconData] = None
    """
    The name of the icon displayed in the corner of the dialog when \
    :attr:`entry_mode` is :attr:`flet.DatePickerEntryMode.INPUT`.

    Clicking on this icon changes the `entry_mode` to
    :attr:`flet.DatePickerEntryMode.CALENDAR`.

    If `None`, `Icons.CALENDAR_TODAY` is used.
    """

    switch_to_input_icon: Optional[IconData] = None
    """
    The name of the icon displayed in the corner of the dialog when \
    :attr:`entry_mode` is :attr:`flet.DatePickerEntryMode.CALENDAR`.

    Clicking on this icon changes the `entry_mode` to
    :attr:`flet.DatePickerEntryMode.INPUT`.

    If `None`, `Icons.EDIT_OUTLINED` is used.
    """

    barrier_color: Optional[ColorValue] = None
    """
    The color of the modal barrier that darkens everything below the date picker.

    If `None`, the :attr:`flet.DialogTheme.barrier_color` is used.
    If it is also `None`, then `Colors.BLACK_54` is used.
    """

    on_change: Optional[ControlEventHandler["DateRangePicker"]] = None
    """
    Called when user clicks confirm button.

    :attr:`start_value` and :attr:`end_value` are updated with selected dates.

    The :attr:`~flet.Event.data` property of the event handler
    argument contains the selected dates.
    """
