import flet as ft

name = "Basic ElevatedButtons"


def example():
    return ft.Column(
        controls=[
            ft.ElevatedButton(content="Elevated button"),
            ft.ElevatedButton("Disabled button", disabled=True),
        ]
    )
