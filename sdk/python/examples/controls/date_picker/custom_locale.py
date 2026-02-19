import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Button(
            content="Pick date (zh_Hans locale)",
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=lambda e: page.show_dialog(
                ft.DatePicker(locale=ft.Locale("zh", "Hans"))
            ),
        )
    )


ft.run(main)
