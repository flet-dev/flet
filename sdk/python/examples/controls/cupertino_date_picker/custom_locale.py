import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.CupertinoFilledButton(
            content="Open CupertinoDatePicker (zh_Hans locale)",
            on_click=lambda e: page.show_dialog(
                ft.CupertinoBottomSheet(
                    height=216,
                    padding=ft.Padding.only(top=6),
                    content=ft.CupertinoDatePicker(
                        locale=ft.Locale("zh", "Hans"),
                        date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
                    ),
                )
            ),
        ),
    )


ft.run(main)
