import flet as ft

name = "TextButtons with icons"


def example():
    return ft.Column(
        [
            ft.TextButton("Button with icon", icon="chair_outlined"),
            ft.TextButton(
                "Button with colorful icon",
                icon="park_rounded",
                icon_color="green400",
            ),
        ]
    )
