import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Column(
            spacing=0,
            expand=True,
            controls=[
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.AMBER,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Divider(),
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.PINK,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Divider(height=1, color=ft.Colors.WHITE),
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.BLUE_300,
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Divider(height=9, thickness=3),
                ft.Container(
                    expand=True,
                    bgcolor=ft.Colors.DEEP_PURPLE_200,
                    alignment=ft.Alignment.CENTER,
                ),
            ],
        ),
    )


ft.run(main)
