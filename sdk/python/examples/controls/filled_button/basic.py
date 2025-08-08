import flet as ft


def main(page: ft.Page):
    page.title = "FilledButton Example"

    page.add(
        ft.FilledButton(content="Filled button"),
        ft.FilledButton(content="Disabled button", disabled=True),
        ft.FilledButton(content="Button with icon", icon=ft.Icons.ADD_OUTLINED),
    )


ft.run(main)
