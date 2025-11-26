import flet as ft

name = "Buttons with icons"


def example():
    return ft.Column(
        controls=[
            ft.Button("Button with icon", icon="chair_outlined"),
            ft.Button(
                "Button with colorful icon",
                icon="park_rounded",
                icon_color="green400",
            ),
        ]
    )
