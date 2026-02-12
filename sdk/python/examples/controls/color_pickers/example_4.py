import flet as ft
from flet_color_pickers import MaterialPicker


def main(page: ft.Page):
    page.title = "MaterialPicker"
    page.padding = 20

    def on_color_change(e: ft.ControlEvent):
        print(f"color: {e.data}")

    def on_primary_change(e: ft.ControlEvent):
        print(f"primary: {e.data}")

    picker = MaterialPicker(
        color="#ff9800",
        on_color_change=on_color_change,
        on_primary_change=on_primary_change,
    )

    page.add(picker)


ft.run(main)
