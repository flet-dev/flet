from datetime import time

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    time_picker = ft.TimePicker(
        value=time(hour=19, minute=30),
        help_text="Pick meeting time",
    )

    def open_picker(hour_format: ft.TimePickerHourFormat):
        time_picker.hour_format = hour_format
        page.show_dialog(time_picker)

    def showcase_card(hour_format: ft.TimePickerHourFormat) -> ft.Container:
        return ft.Container(
            width=300,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(hour_format.name, weight=ft.FontWeight.BOLD),
                    ft.Button(
                        "Open TimePicker",
                        icon=ft.Icons.SCHEDULE,
                        on_click=lambda _, f=hour_format: open_picker(f),
                    ),
                ],
            ),
        )

    page.appbar = ft.AppBar(title="TimePickerHourFormat Showcase")
    page.add(
        ft.Text("Open the picker to compare 12h, 24h, and system modes."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                showcase_card(hour_format) for hour_format in ft.TimePickerHourFormat
            ],
        ),
    )


ft.run(main)
