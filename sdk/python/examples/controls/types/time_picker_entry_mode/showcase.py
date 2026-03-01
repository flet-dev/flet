from datetime import time

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    picker = ft.TimePicker(value=time(hour=19, minute=30))

    def open_picker(entry_mode: ft.TimePickerEntryMode):
        picker.entry_mode = entry_mode
        page.show_dialog(picker)

    def showcase_card(entry_mode: ft.TimePickerEntryMode) -> ft.Container:
        return ft.Container(
            width=320,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(entry_mode.name, weight=ft.FontWeight.BOLD),
                    ft.Button(
                        "Open TimePicker",
                        icon=ft.Icons.SCHEDULE,
                        on_click=lambda _, m=entry_mode: open_picker(m),
                    ),
                ],
            ),
        )

    page.appbar = ft.AppBar(title="TimePickerEntryMode Showcase")
    page.add(
        ft.Text("Open the picker to compare dial/input entry modes."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(m) for m in ft.TimePickerEntryMode],
        ),
    )


ft.run(main)
