import flet as ft


def main(page: ft.Page):
    page.title = "TextButtons with icons"

    page.add(
        ft.TextButton(content="Button with icon", icon=ft.Icons.WAVES_OUTLINED),
        ft.TextButton(
            content="Button with colorful icon",
            icon=ft.Icons.PARK_ROUNDED,
            icon_color=ft.Colors.GREEN_400,
        ),
    )


ft.run(main)
