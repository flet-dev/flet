import flet as ft

name = "Dropdown with label and hint"


def example():
    return ft.Dropdown(
        label="Color",
        hint_text="Choose your favourite color?",
        options=[
            ft.dropdown.Option("Red"),
            ft.dropdown.Option("Green"),
            ft.dropdown.Option("Blue"),
        ],
        autofocus=True,
    )
