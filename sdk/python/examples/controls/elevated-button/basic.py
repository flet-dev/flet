import flet as ft


def main(page: ft.Page):
    page.title = "ElevatedButton Example"

    page.add(
        ft.ElevatedButton(content="Elevated button"),
        ft.ElevatedButton(content="Disabled button", disabled=True),
    )


ft.run(main)
