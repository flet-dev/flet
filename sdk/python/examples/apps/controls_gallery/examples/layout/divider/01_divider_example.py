import flet as ft

name = "Divider example"


def example():
    return ft.Column(
        [
            ft.Container(
                bgcolor=ft.Colors.AMBER,
                alignment=ft.Alignment.CENTER,
                expand=1,
            ),
            ft.Divider(),
            ft.Container(
                bgcolor=ft.Colors.PINK, alignment=ft.Alignment.CENTER, expand=1
            ),
            ft.Divider(height=1, color="white"),
            ft.Container(
                bgcolor=ft.Colors.BLUE_300,
                alignment=ft.Alignment.CENTER,
                expand=1,
            ),
            ft.Divider(height=9, thickness=3),
            ft.Container(
                bgcolor=ft.Colors.DEEP_PURPLE_200,
                alignment=ft.Alignment.CENTER,
                expand=1,
            ),
        ],
        spacing=0,
        width=400,
        height=400,
    )
