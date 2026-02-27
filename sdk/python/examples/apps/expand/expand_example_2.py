import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Row(
            controls=[
                ft.Container(content=ft.Text("A"), expand=1),
                ft.Container(content=ft.Text("B"), expand=3),
                ft.Container(content=ft.Text("C"), expand=1),
            ]
        )
    )


ft.run(main)
