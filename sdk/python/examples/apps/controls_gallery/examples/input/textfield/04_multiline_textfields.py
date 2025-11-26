import flet as ft

name = "Multiline TextFields"


def example():
    return ft.Column(
        controls=[
            ft.TextField(label="standard", multiline=True),
            ft.TextField(
                label="disabled",
                multiline=True,
                disabled=True,
                value="line1\nline2\nline3\nline4\nline5",
            ),
            ft.TextField(
                label="Auto adjusted height with max lines",
                multiline=True,
                min_lines=1,
                max_lines=3,
            ),
        ]
    )
