import flet as ft

name = "Placeholder example"


def example():
    return ft.Placeholder(
        expand=True, color=ft.Colors.random()
    )  # random material color
