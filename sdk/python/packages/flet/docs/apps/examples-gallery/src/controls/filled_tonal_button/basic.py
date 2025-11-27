import flet as ft


def main(page: ft.Page):
    page.title = "FilledTonalButton Example"

    page.add(
        ft.FilledTonalButton(content="Filled tonal button"),
        ft.FilledTonalButton(content="Disabled button", disabled=True),
        ft.FilledTonalButton(content="Button with icon", icon=ft.Icons.ADD_OUTLINED),
    )


if __name__ == "__main__":
    ft.run(main)
