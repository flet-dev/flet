from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from flet.controls.material.textfield import KeyboardType
from flet.core.control import Control, control
from flet.core.control_event import ControlEvent
from flet.core.types import (
    DateTimeValue,
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
    entry_mode: Optional[DatePickerEntryMode] = None


@control("DatePicker")
class DatePicker(Control):
    """
    A Material-style date picker dialog.

    It is added to [`page.overlay`](page#overlay) and can be opened by setting `open=True` or by calling `Page.open()` method.

    Depending on the `date_picker_entry_mode`, it will show either a Calendar or an Input (TextField) for picking a date.

    Example:
    ```
    import flet as ft


    def main(page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def handle_date_change(e: ft.ControlEvent):
            page.add(ft.Text(f"Date changed: {e.control.value.strftime('%Y-%m-%d %H:%M %p')}"))

        cupertino_date_picker = ft.CupertinoDatePicker(
            date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
            on_change=handle_date_change,
        )
        page.add(
            ft.CupertinoFilledButton(
                "Open CupertinoDatePicker",
                on_click=lambda e: page.open(
                    ft.CupertinoBottomSheet(
                        cupertino_date_picker,
                        height=216,
                        padding=ft.padding.only(top=6),
                    )
                ),
            )
        )


    ft.app(main)
    ```

    -----

    Online docs: https://flet.dev/docs/controls/datepicker
    """

    open: bool = False
    value: Optional[DateTimeValue] = None
    first_date: DateTimeValue = datetime(year=1900, month=1, day=1)
    last_date: DateTimeValue = datetime(year=2050, month=1, day=1)
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
    on_dismiss: OptionalControlEventCallable = None
    on_entry_mode_change: OptionalEventCallable[DatePickerEntryModeChangeEvent] = None
