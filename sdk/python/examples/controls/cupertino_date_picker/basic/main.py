from datetime import datetime

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    message = ft.Text("Chosen Time:")

    def handle_date_change(e: ft.Event[ft.CupertinoDatePicker]):
        message.value = f"Chosen Date: {e.control.value.strftime('%Y-%m-%d %H:%M %p')}"

    cupertino_date_picker = ft.CupertinoDatePicker(
        value=datetime.now(),
        date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
        on_change=handle_date_change,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.CupertinoFilledButton(
                        on_click=lambda _: page.show_dialog(
                            ft.CupertinoBottomSheet(
                                height=216,
                                padding=ft.Padding.only(top=6),
                                content=cupertino_date_picker,
                            )
                        ),
                        content="Open CupertinoDatePicker",
                    ),
                    message,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
