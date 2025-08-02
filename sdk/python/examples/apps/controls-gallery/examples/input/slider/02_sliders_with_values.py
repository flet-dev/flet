import flet as ft

name = "Sliders with values"


def example():
    return ft.Column(
        controls=[
            ft.Text("Slider with value:"),
            ft.Slider(value=0.3),
            ft.Text("Slider with a custom range and label:"),
            ft.Slider(min=0, max=100, divisions=10, label="{value}%"),
        ]
    )
