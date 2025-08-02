import flet as ft


def main(page: ft.Page):
    page.add(
        ft.TextField(
            label="Password with reveal button",
            password=True,
            can_reveal_password=True,
        )
    )


ft.run(main)
