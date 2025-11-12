from datetime import time

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def get_system_hour_format():
        """Returns the current system's hour format."""
        return "24h" if page.media.always_use_24_hour_format else "12h"

    def format_time(value: time) -> str:
        """Returns a formatted time string based on TimePicker and system settings."""
        use_24h = time_picker.hour_format == ft.TimePickerHourFormat.H24 or (
            time_picker.hour_format == ft.TimePickerHourFormat.SYSTEM
            and page.media.always_use_24_hour_format
        )
        return value.strftime("%H:%M" if use_24h else "%I:%M %p")

    def handle_change(e: ft.Event[ft.TimePicker]):
        selection.value = f"Selection: {format_time(time_picker.value)}"

    time_picker = ft.TimePicker(
        value=time(hour=19, minute=30),
        help_text="Choose your meeting time",
        on_change=handle_change,
    )

    def open_picker(e: ft.Event[ft.Button]):
        choice = format_dropdown.value
        hour_format_map = {
            "system": ft.TimePickerHourFormat.SYSTEM,
            "12h": ft.TimePickerHourFormat.H12,
            "24h": ft.TimePickerHourFormat.H24,
        }
        time_picker.hour_format = hour_format_map[choice]
        page.show_dialog(time_picker)

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                format_dropdown := ft.Dropdown(
                    label="Hour format",
                    value="system",
                    width=260,
                    key="dd",
                    options=[
                        ft.DropdownOption(
                            key="system",
                            text=f"System default ({get_system_hour_format()})",
                        ),
                        ft.DropdownOption(key="12h", text="12-hour clock"),
                        ft.DropdownOption(key="24h", text="24-hour clock"),
                    ],
                ),
                ft.Button(
                    "Open TimePicker",
                    icon=ft.Icons.SCHEDULE,
                    on_click=open_picker,
                ),
            ],
        ),
        selection := ft.Text(weight=ft.FontWeight.BOLD),
    )


if __name__ == "__main__":
    ft.run(main)
