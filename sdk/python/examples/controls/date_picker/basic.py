import datetime

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_change(e: ft.Event[ft.DatePicker]):
        page.add(ft.Text(f"Date changed: {e.control.value.strftime('%m/%d/%Y')}"))

    def handle_dismissal(e: ft.Event[ft.DatePicker]):
        page.add(ft.Text("DatePicker dismissed"))

    page.add(
        ft.ElevatedButton(
            content="Pick date",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.show_dialog(
                ft.DatePicker(
                    first_date=datetime.datetime(year=2000, month=10, day=1),
                    last_date=datetime.datetime(year=2025, month=10, day=1),
                    on_change=handle_change,
                    on_dismiss=handle_dismissal,
                )
            ),
        )
    )


ft.run(main)
