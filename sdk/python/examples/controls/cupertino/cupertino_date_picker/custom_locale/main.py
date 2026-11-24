import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.SafeArea(
            content=ft.CupertinoFilledButton(
                on_click=lambda _: page.show_dialog(
                    ft.CupertinoBottomSheet(
                        height=216,
                        padding=ft.Padding.only(top=6),
                        content=ft.CupertinoDatePicker(
                            locale=ft.Locale("zh", "Hans"),
                            date_picker_mode=ft.CupertinoDatePickerMode.DATE_AND_TIME,
                        ),
                    )
                ),
                content="Open CupertinoDatePicker (zh_Hans locale)",
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
