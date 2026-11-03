import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Container(
            content=ft.Text("👋 Hello from Flet!", size=16),
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
    )


ft.run(main)
