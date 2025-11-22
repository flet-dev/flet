import flet as ft

name = "TextFields with prefixes and suffixes"


def example():
    return ft.Column(
        controls=[
            ft.TextField(label="With prefix", prefix="https://"),
            ft.TextField(label="With suffix", suffix=".com"),
            ft.TextField(
                label="With prefix and suffix",
                prefix="https://",
                suffix=".com",
            ),
            ft.TextField(
                label="My favorite color",
                icon=ft.Icons.FORMAT_SIZE,
                hint_text="Type your favorite color",
                helper="You can type only one color",
                counter="0 symbols typed",
                prefix_icon=ft.Icons.COLOR_LENS,
                suffix="...is your color",
            ),
        ]
    )
