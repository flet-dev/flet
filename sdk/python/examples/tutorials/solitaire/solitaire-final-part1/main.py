import flet as ft
from solitaire import Solitaire


def main(page: ft.Page):
    page.on_error = lambda e: print("Page error:", e.data)

    solitaire = Solitaire()

    page.add(solitaire)


ft.app(target=main, assets_dir="assets")
