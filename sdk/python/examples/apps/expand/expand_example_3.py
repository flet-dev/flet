import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Container(
            width=500,
            height=180,
            padding=10,
            border=ft.Border.all(2, ft.Colors.BLUE_GREY_200),
            border_radius=10,
            content=ft.Row(
                spacing=8,
                controls=[
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.ORANGE_300,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("Card 1"),
                    ),
                    ft.Container(
                        expand=True,
                        bgcolor=ft.Colors.GREEN_200,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER,
                        content=ft.Text("Card 2"),
                    ),
                ],
            ),
        )
    )


ft.run(main)
