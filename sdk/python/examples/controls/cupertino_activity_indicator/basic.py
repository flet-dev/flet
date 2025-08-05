import flet as ft


def main(page: ft.Page):
    page.add(
        ft.CupertinoActivityIndicator(
            animating=True,
            color=ft.Colors.RED,
            radius=50,
        )
    )


ft.run(main)
