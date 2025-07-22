import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Placeholder(
            expand=True,
            color=ft.Colors.random(),
        )
    )


ft.run(main)
