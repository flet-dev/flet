from dataclasses import dataclass, field
from datetime import datetime, time
from enum import Enum
from typing import Optional

from flet.controls.base_control import control
from flet.controls.control_event import (
    ControlEventHandler,
    Event,
    EventHandler,
)
from flet.controls.dialog_control import DialogControl
from flet.controls.icon_data import IconData
from flet.controls.types import (
    ColorValue,
    Locale,
    Orientation,
)

__all__ = [
    "TimePicker",
    "TimePickerEntryMode",
    "TimePickerEntryModeChangeEvent",
    "TimePickerHourFormat",
]


class TimePickerHourFormat(Enum):
    """
    Defines the hour format for the [`TimePicker`][flet.] control.
    """

    SYSTEM = "system"
    """Respect the host platform setting."""

    H12 = "h12"
    """A 12-hour clock with an AM/PM selector."""

    H24 = "h24"
    """A 24-hour clock without an AM/PM selector."""


class TimePickerEntryMode(Enum):
    """
    Interactive input mode of the [`TimePicker`][flet.] dialog.

    In [`DIAL`][(c).] mode, a clock dial is displayed, and the user taps or drags
    the time they wish to select. In [`INPUT`][(c).] mode, [`TextField`][flet.]s are
    displayed and the user types in the time they wish to select.
    """

    DIAL = "dial"
    """
    User picks time from a clock dial.

    Can switch to [`INPUT`][(c).] by activating a mode button in the time picker dialog.
    """

    INPUT = "input"
    """
    User can input the time by typing it into text fields.

    Can switch to [`DIAL`][(c).] by activating a mode button in the time picker dialog.
    """

    DIAL_ONLY = "dialOnly"
    """
    User can only pick time from a clock dial.

    There is no user interface to switch to another mode.
    """

    INPUT_ONLY = "inputOnly"
    """
    User can only input the time by typing it into text fields.

    There is no user interface to switch to another mode.
    """


@dataclass
class TimePickerEntryModeChangeEvent(Event["TimePicker"]):
    """
    Represents the event triggered when the
    entry mode of a [`TimePicker`][flet.] changes.
    """

    entry_mode: TimePickerEntryMode
    """The new entry mode."""


@control("TimePicker")
class TimePicker(DialogControl):
    """
    A Material-style time picker dialog.

    Can be opened by calling the
    [`Page.show_dialog()`][flet.Page.show_dialog] method.

    Depending on the [`entry_mode`][(c).], it will show either a Dial or
    an Input (hour and minute text fields) for picking a time.

    Example:
    ```python
    ft.TimePicker(
        open=True,
        value=time(1, 2),
        entry_mode=ft.TimePickerEntryMode.INPUT_ONLY,
    )
    ```
    """

    value: Optional[time] = field(default_factory=lambda: datetime.now().time())
    """
    The selected time that this picker should display.

    The default value is equal to the current time.
    """

    locale: Optional[Locale] = None
    """
    The locale for this time picker dialog. It is intended for (rare) cases where this
    dialog should be localized differently from the rest of the page.

    It overrides the locale used by the page (see [`Page.locale_configuration`][flet.]),
    but does not participate in page-level locale resolution.

    If set to `None` (the default) or an inexistent/unsupported locale,
    the [`current_locale`][flet.LocaleConfiguration.] of the
    [`Page.locale_configuration`][flet.] is used as fallback.
    """

    modal: bool = False
    """
    Whether this picker cannot be dismissed by clicking the area outside of it.
    """

    entry_mode: TimePickerEntryMode = TimePickerEntryMode.DIAL
    """
    The initial mode of time entry method for this picker.

    Defaults to [`TimePickerEntryMode.DIAL`][flet.].
    """

    hour_label_text: Optional[str] = None
    """
    The text that is displayed below the hour input text field.

    The default value is `"Hour"`.
    """

    minute_label_text: Optional[str] = None
    """
    The text that is displayed below the minute input text field.

    The default value is `"Minute"`.
    """

    help_text: Optional[str] = None
    """
    The text that is displayed at the top of the header.

    This is used to indicate to the user what they are selecting a time for.
    The default value is `"Enter time"`.
    """

    cancel_text: Optional[str] = None
    """
    The text that is displayed on the cancel button.

    The default value is `"Cancel"`.
    """

    confirm_text: Optional[str] = None
    """
    The text that is displayed on the confirm button.

    The default value is `"OK"`.
    """

    error_invalid_text: Optional[str] = None
    """
    The error message displayed below the input text field if the input is not a
    valid hour/minute.

    The default value is `"Enter a valid time"`.
    """

    orientation: Optional[Orientation] = None
    """
    The orientation of the dialog when displayed.
    """

    barrier_color: Optional[ColorValue] = None
    """
    The color of the modal barrier that darkens everything below this picker's dialog.

    If `None`, the [`DialogTheme.barrier_color`][flet.] is used.
    If it is also `None`, then [`Colors.BLACK_54`][flet.] is used.
    """

    switch_to_timer_icon: Optional[IconData] = None
    """
    The icon displayed in the corner of this picker's dialog when
    [`entry_mode`][(c).] is [`TimePickerEntryMode.INPUT`][flet.].

    Clicking on this icon changes the [`entry_mode`][(c).] to
    [`TimePickerEntryMode.DIAL`][flet.].

    If `None`, defaults to [`Icons.ACCESS_TIME`][flet.].
    """

    switch_to_input_icon: Optional[IconData] = None
    """
    The icon displayed in the corner of this picker's dialog when
    [`entry_mode`][(c).] is [`TimePickerEntryMode.DIAL`][flet.].

    Clicking on icon changes the [`entry_mode`][(c).] to
    [`TimePickerEntryMode.INPUT`][flet.].

    If `None`, defaults to [`Icons.KEYBOARD_OUTLINED`][flet.].
    """

    on_change: Optional[ControlEventHandler["TimePicker"]] = None
    """
    Called when user clicks confirm button.

    [`value`][(c).] property is updated with selected time.
    Additionally, the [`data`][flet.Event.] property of the event handler argument
    also contains the selected time.
    """

    on_entry_mode_change: Optional[EventHandler[TimePickerEntryModeChangeEvent]] = None
    """
    Called when the [`entry_mode`][(c).] is changed through the time picker dialog.
    """

    hour_format: TimePickerHourFormat = TimePickerHourFormat.SYSTEM
    """
    Defines the hour format of this time picker.
    """
