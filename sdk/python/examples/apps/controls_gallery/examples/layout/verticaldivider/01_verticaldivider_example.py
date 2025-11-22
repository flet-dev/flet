import flet as ft

name = "VerticalDivider example"


def example():
    return ft.Row(
        [
            ft.Container(
                bgcolor=ft.Colors.ORANGE_300,
                alignment=ft.Alignment.CENTER,
                expand=1,
            ),
            ft.VerticalDivider(),
            ft.Container(
                bgcolor=ft.Colors.BROWN_400,
                alignment=ft.Alignment.CENTER,
                expand=1,
            ),
            ft.VerticalDivider(width=1, color="white"),
            ft.Container(
                bgcolor=ft.Colors.BLUE_300,
                alignment=ft.Alignment.CENTER,
                expand=1,
            ),
            ft.VerticalDivider(width=9, thickness=3),
            ft.Container(
                bgcolor=ft.Colors.GREEN_300,
                alignment=ft.Alignment.CENTER,
                expand=1,
            ),
        ],
        spacing=0,
        width=400,
        height=400,
    )
