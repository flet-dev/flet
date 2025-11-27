import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Button(content="Enabled button"),
        ft.Button(content="Disabled button", disabled=True),
    )


if __name__ == "__main__":
    ft.run(main)
