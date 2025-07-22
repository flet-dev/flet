import flet as ft


def main(page: ft.Page):
    page.add(ft.Text(value="Hello, world!"))


ft.app(target=main)
