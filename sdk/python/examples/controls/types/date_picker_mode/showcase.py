import datetime

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    today = datetime.datetime.now()
    picker = ft.DatePicker(
        first_date=datetime.datetime(year=today.year - 1, month=1, day=1),
        last_date=datetime.datetime(year=today.year + 1, month=12, day=31),
        entry_mode=ft.DatePickerEntryMode.CALENDAR,
    )

    def open_picker(date_picker_mode: ft.DatePickerMode):
        picker.date_picker_mode = date_picker_mode
        page.show_dialog(picker)

    def showcase_card(date_picker_mode: ft.DatePickerMode) -> ft.Container:
        return ft.Container(
            width=320,
            padding=12,
            border=ft.Border.all(1, ft.Colors.RED),
            border_radius=10,
            bgcolor=ft.Colors.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                spacing=8,
                controls=[
                    ft.Text(date_picker_mode.name, weight=ft.FontWeight.BOLD),
                    ft.Button(
                        "Open DatePicker",
                        icon=ft.Icons.CALENDAR_MONTH,
                        on_click=lambda _, m=date_picker_mode: open_picker(m),
                    ),
                ],
            ),
        )

    page.appbar = ft.AppBar(title="DatePickerMode Showcase")
    page.add(
        ft.Text("Open the picker to compare initial day vs year display mode."),
        ft.Row(
            wrap=True,
            spacing=12,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[showcase_card(m) for m in ft.DatePickerMode],
        ),
    )


ft.run(main)
