import flet as ft

name = "Containers with different alignment"


def example():
    container_1 = ft.Container(
        content=ft.Text("Center"),
        alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.BLUE_GREY_100,
        width=150,
        height=150,
    )

    container_2 = ft.Container(
        content=ft.Text("Top left"),
        alignment=ft.Alignment.TOP_LEFT,
        bgcolor=ft.Colors.BLUE_GREY_200,
        width=150,
        height=150,
    )

    container_3 = ft.Container(
        content=ft.Text("-0.5, -0.5"),
        alignment=ft.alignment.Alignment(-0.5, -0.5),
        bgcolor=ft.Colors.BLUE_GREY_300,
        width=150,
        height=150,
    )

    return ft.Row(controls=[container_1, container_2, container_3])
