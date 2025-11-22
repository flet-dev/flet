import flet as ft

name = "Basic TextButtons"


def example():
    return ft.Column(
        [
            ft.TextButton(content="Text button"),
            ft.TextButton("Disabled button", disabled=True),
        ]
    )
