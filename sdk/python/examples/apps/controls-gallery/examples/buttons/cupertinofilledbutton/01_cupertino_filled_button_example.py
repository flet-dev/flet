import flet as ft

name = "CupertinoFilledButton example"


def example():
    button = ft.CupertinoFilledButton(
        content=ft.Text("CupertinoButton"),
        opacity_on_click=0.3,
        on_click=lambda e: print("CupertinoFilledButton clicked!"),
    )

    return button
