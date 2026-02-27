import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Container(
            width=500,
            height=180,
            content=ft.Row(
                controls=[
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.ORANGE_300,
                        content=ft.Text("Card 1"),
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.GREEN_100,
                        content=ft.Text("Card 2"),
                    ),
                ],
            ),
        )
    )


ft.run(main)
