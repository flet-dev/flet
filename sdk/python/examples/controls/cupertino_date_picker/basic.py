from datetime import datetime

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_date_change(e: ft.Event[ft.CupertinoDatePicker]):
        message.value = f"Chosen Date: {e.control.value.strftime('%Y-%m-%d %H:%M %p')}"
        page.update()

    cupertino_date_picker = ft.CupertinoDatePicker(
        value=datetime.now(),
        date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
        on_change=handle_date_change,
    )

    page.add(
        ft.CupertinoFilledButton(
            content="Open CupertinoDatePicker",
            on_click=lambda e: page.show_dialog(
                ft.CupertinoBottomSheet(
                    content=cupertino_date_picker,
                    height=216,
                    padding=ft.Padding.only(top=6),
                )
            ),
        ),
        message := ft.Text("Chosen Time: "),
    )


ft.run(main)
