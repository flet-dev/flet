from dataclasses import field
from datetime import datetime, time
from enum import Enum
from typing import Optional

from flet.controls.control import control
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

    It is added to [`page.overlay`](page#overlay) and can be opened by setting `open=True` or by calling `Page.open()` method.

    Depending on the `time_picker_entry_mode`, it will show either a Dial or an Input (hour and minute text fields) for picking a time.

    Example:
    ```
    import flet as ft


    def main(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

        def handle_change(e):
            page.add(ft.Text(f"TimePicker change: {time_picker.value}"))

        def handle_dismissal(e):
            page.add(ft.Text(f"TimePicker dismissed: {time_picker.value}"))

        def handle_entry_mode_change(e):
            page.add(ft.Text(f"TimePicker Entry mode changed to {e.entry_mode}"))

        time_picker = ft.TimePicker(
            confirm_text="Confirm",
            error_invalid_text="Time out of range",
            help_text="Pick your time slot",
            on_change=handle_change,
            on_dismiss=handle_dismissal,
            on_entry_mode_change=handle_entry_mode_change,
        )

        page.add(
            ft.ElevatedButton(
                "Pick time",
                icon=ft.icons.TIME_TO_LEAVE,
                on_click=lambda _: page.open(time_picker),
            )
        )


    ft.app(main)
    ```

    -----

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
