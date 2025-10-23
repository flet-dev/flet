import flet as ft
from datetime import time


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_change(e: ft.Event[ft.TimePicker]):
        page.add(ft.Text(f"TimePicker change: {time_picker.value}"))

    def handle_dismissal(e: ft.Event[ft.TimePicker]):
        page.add(ft.Text(f"TimePicker dismissed: {time_picker.value}"))

    def handle_entry_mode_change(e: ft.TimePickerEntryModeChangeEvent):
        page.add(ft.Text(f"TimePicker Entry mode changed to {e.entry_mode}"))

    time_picker = ft.TimePicker(
        value=time(1, 2),
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        on_change=handle_change,
        on_dismiss=handle_dismissal,
        on_entry_mode_change=handle_entry_mode_change,
    )

    page.add(
        ft.Button(
            content="Pick time",
            icon=ft.Icons.TIME_TO_LEAVE,
            on_click=lambda _: page.show_dialog(time_picker),
        )
    )


if __name__ == "__main__":
    ft.run(main)
