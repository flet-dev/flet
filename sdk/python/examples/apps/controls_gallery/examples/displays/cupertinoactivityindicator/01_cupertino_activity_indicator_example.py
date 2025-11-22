import flet as ft

name = "CupertinoActivityIndicator Example"


def example():
    return ft.CupertinoActivityIndicator(
        radius=50,
        color=ft.Colors.RED,
        animating=True,
    )
