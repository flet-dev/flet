import flet as ft

name = "Containers with different gradient backgrounds"


def example():
    import math

    container_1 = ft.Container(
        content=ft.Text("LinearGradient"),
        alignment=ft.Alignment.CENTER,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.top_CENTER,
            end=ft.Alignment.bottom_CENTER,
            colors=[ft.Colors.BLUE, ft.Colors.YELLOW],
        ),
        width=150,
        height=150,
        border_radius=5,
    )

    container_2 = ft.Container(
        content=ft.Text("RadialGradient"),
        alignment=ft.Alignment.CENTER,
        gradient=ft.RadialGradient(
            colors=[ft.Colors.YELLOW, ft.Colors.BLUE],
        ),
        width=150,
        height=150,
        border_radius=5,
    )

    container_3 = ft.Container(
        content=ft.Text("SweepGradient"),
        alignment=ft.Alignment.CENTER,
        gradient=ft.SweepGradient(
            center=ft.Alignment.CENTER,
            start_angle=0.0,
            end_angle=math.pi * 2,
            colors=[ft.Colors.YELLOW, ft.Colors.BLUE],
        ),
        width=150,
        height=150,
        border_radius=5,
    )

    return ft.Row(controls=[container_1, container_2, container_3])
