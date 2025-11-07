from datetime import time

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_change(e: ft.Event[ft.TimePicker]):
        fmt = (
            "%H:%M"
            if time_picker.hour_format == ft.TimePickerHourFormat.H24
            else "%I:%M %p"
        )
        selection.value = f"Selection: {time_picker.value.strftime(fmt)}"

    time_picker = ft.TimePicker(
        value=time(hour=9, minute=30),
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
                    width=210,
                    options=[
                        ft.DropdownOption(key="system", text="System default"),
                        ft.DropdownOption(key="12h", text="12-hour clock"),
                        ft.DropdownOption(key="24h", text="24-hour clock"),
                    ],
                ),
                ft.Button(
                    "Open TimePicker", icon=ft.Icons.SCHEDULE, on_click=open_picker
                ),
            ],
        ),
        selection := ft.Text(weight=ft.FontWeight.BOLD),
    )


if __name__ == "__main__":
    ft.run(main)
