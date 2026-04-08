import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.SafeArea(
            content=ft.Button(
                content="Pick time (zh_Hans locale)",
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda e: page.show_dialog(
                    ft.TimePicker(locale=ft.Locale("zh", "Hans"))
                ),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
