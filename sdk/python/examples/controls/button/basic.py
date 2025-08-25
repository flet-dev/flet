import flet as ft


def main(page: ft.Page):
    page.title = "Button Example"

    page.add(
        ft.Button(content="Elevated button"),
        ft.Button(content="Disabled button", disabled=True),
    )


ft.run(main)
