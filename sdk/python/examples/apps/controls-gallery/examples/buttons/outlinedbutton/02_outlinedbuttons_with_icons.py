import flet as ft

name = "OutlinedButtons with icons"


def example():
    return ft.Column(
        [
            ft.OutlinedButton(
                content="Button with icon",
                icon=ft.Icons.CHAIR_OUTLINED,
            ),
            ft.OutlinedButton(
                "Button with colorful icon",
                # icon=ft.Icons.PARK_ROUNDED,
                icon_color="green400",
            ),
        ]
    )
