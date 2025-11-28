import flet as ft

name = "CupertinoButton example"


def example():
    button = ft.CupertinoButton(
        content=ft.Text("CupertinoButton"),
        opacity_on_click=0.3,
        on_click=lambda e: print("Normal CupertinoButton clicked!"),
    )

    return button
