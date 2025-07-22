import flet as ft
from example import Example


def main(page: ft.Page):
    page.add(Example())
    page.update()


ft.app(target=main)
