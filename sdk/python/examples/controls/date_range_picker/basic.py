import datetime

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_change(e: ft.Event[ft.DateRangePicker]):
        page.add(
            ft.Text(
                f"Start Date changed: {e.control.start_value.strftime('%m/%d/%Y')}"
            ),
            ft.Text(f"End Date changed: {e.control.end_value.strftime('%m/%d/%Y')}"),
        )

    def handle_dismissal(e: ft.Event[ft.DialogControl]):
        page.add(ft.Text("DatePicker dismissed"))

    today = datetime.datetime.now()

    page.add(
        ft.Button(
            content=ft.Text("Pick date"),
            icon=ft.Icons.PHONE,
            on_click=lambda e: page.show_dialog(
                ft.DateRangePicker(
                    start_value=datetime.datetime(
                        year=today.year, month=today.month, day=1
                    ),
                    end_value=datetime.datetime(
                        year=today.year, month=today.month, day=15
                    ),
                    on_change=handle_change,
                    on_dismiss=handle_dismissal,
                )
            ),
        )
    )


ft.run(main)
