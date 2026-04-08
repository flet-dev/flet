import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.SafeArea(
            content=ft.Button(
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda _: page.show_dialog(
                    ft.DateRangePicker(locale=ft.Locale("zh", "Hans"))
                ),
                content="Pick dates (zh_Hans locale)",
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
