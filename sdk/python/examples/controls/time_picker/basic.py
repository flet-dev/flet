from datetime import time

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_change(e: ft.Event[ft.TimePicker]):
        selection.value = f"Selection: {time_picker.value}"
        page.show_dialog(ft.SnackBar(f"TimePicker change: {time_picker.value}"))

    def handle_dismissal(e: ft.Event[ft.TimePicker]):
        page.show_dialog(ft.SnackBar("TimePicker dismissed!"))

    def handle_entry_mode_change(e: ft.TimePickerEntryModeChangeEvent):
        page.show_dialog(ft.SnackBar(f"Entry mode changed: {time_picker.entry_mode}"))

    time_picker = ft.TimePicker(
        value=time(hour=19, minute=30),
        confirm_text="Confirm",
        error_invalid_text="Time out of range",
        help_text="Pick your time slot",
        entry_mode=ft.TimePickerEntryMode.DIAL,
        on_change=handle_change,
        on_dismiss=handle_dismissal,
        on_entry_mode_change=handle_entry_mode_change,
    )

    page.add(
        ft.Button(
            content="Pick time",
            icon=ft.Icons.TIME_TO_LEAVE,
            on_click=lambda: page.show_dialog(time_picker),
        ),
        selection := ft.Text(weight=ft.FontWeight.BOLD),
    )


if __name__ == "__main__":
    ft.run(main)
