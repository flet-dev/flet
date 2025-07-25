import flet as ft


def main(page: ft.Page):
    page.title = "Basic text buttons"

    page.add(
        ft.TextButton(content="Text button"),
        ft.TextButton(content="Disabled button", disabled=True),
    )


ft.run(main)
