import flet as ft

name = "Underlined and borderless TextFields"


def example():
    return ft.Column(
        controls=[
            ft.TextField(
                label="Underlined",
                border=ft.InputBorder.UNDERLINE,
                hint_text="Enter text here",
            ),
            ft.TextField(
                label="Underlined filled",
                border=ft.InputBorder.UNDERLINE,
                filled=True,
                hint_text="Enter text here",
            ),
            ft.TextField(
                label="Borderless",
                border=ft.InputBorder.NONE,
                hint_text="Enter text here",
            ),
            ft.TextField(
                label="Borderless filled",
                border=ft.InputBorder.NONE,
                filled=True,
                hint_text="Enter text here",
            ),
        ]
    )
