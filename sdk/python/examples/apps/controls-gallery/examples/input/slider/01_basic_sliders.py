import flet as ft

name = "Basic sliders"


def example():
    return ft.Column(
        controls=[
            ft.Text("Default slider:"),
            ft.Slider(),
            ft.Text("Default disabled slider:"),
            ft.Slider(disabled=True),
        ]
    )
