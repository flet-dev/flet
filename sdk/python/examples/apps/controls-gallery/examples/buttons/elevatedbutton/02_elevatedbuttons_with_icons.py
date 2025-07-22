import flet as ft

name = "ElevatedButtons with icons"


def example():
    return ft.Column(
        controls=[
            ft.ElevatedButton("Button with icon", icon="chair_outlined"),
            ft.ElevatedButton(
                "Button with colorful icon",
                icon="park_rounded",
                icon_color="green400",
            ),
        ]
    )
