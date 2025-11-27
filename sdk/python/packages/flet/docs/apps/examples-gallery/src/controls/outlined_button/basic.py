import flet as ft


def main(page: ft.Page):
    page.title = "OutlinedButton Example"

    page.add(
        ft.OutlinedButton(content="Outlined button"),
        ft.OutlinedButton(content="Disabled button", disabled=True),
    )


if __name__ == "__main__":
    ft.run(main)
