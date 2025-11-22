import flet as ft

name = "Clickable containers"


def example():
    return ft.Row(
        [
            ft.Container(
                content=ft.Text("Non clickable"),
                margin=10,
                padding=10,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.AMBER,
                width=150,
                height=150,
                border_radius=10,
            ),
            ft.Container(
                content=ft.Text("Clickable without Ink"),
                margin=10,
                padding=10,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.GREEN_200,
                width=150,
                height=150,
                border_radius=10,
                on_click=lambda e: print("Clickable without Ink clicked!"),
            ),
            ft.Container(
                content=ft.Text("Clickable with Ink"),
                margin=10,
                padding=10,
                alignment=ft.Alignment.CENTER,
                bgcolor=ft.Colors.CYAN_200,
                width=150,
                height=150,
                border_radius=10,
                ink=True,
                on_click=lambda e: print("Clickable with Ink clicked!"),
            ),
            ft.Container(
                content=ft.Text("Clickable transparent with Ink"),
                margin=10,
                padding=10,
                alignment=ft.Alignment.CENTER,
                width=150,
                height=150,
                border_radius=10,
                ink=True,
                on_click=lambda e: print("Clickable transparent with Ink clicked!"),
            ),
        ],
    )
