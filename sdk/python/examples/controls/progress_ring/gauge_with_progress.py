import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Stack(
            width=100,
            height=100,
            controls=[
                ft.Container(content=ft.Text("60%"), alignment=ft.Alignment.CENTER),
                ft.ProgressRing(value=0.6, width=100, height=100),
            ],
        )
    )


ft.run(main)
