import flet as ft

name = "Transparent title over an image"


def example():
    st = ft.Stack(
        [
            ft.Image(
                src="https://picsum.photos/300/300",
                width=300,
                height=300,
                fit=ft.BoxFit.CONTAIN,
            ),
            ft.Row(
                [
                    ft.Text(
                        "Image title",
                        color="white",
                        size=40,
                        weight="bold",
                        opacity=0.5,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        width=300,
        height=300,
    )

    return st
