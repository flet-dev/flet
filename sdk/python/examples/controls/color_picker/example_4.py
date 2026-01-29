import flet as ft
from flet_color_picker import MaterialPicker


def main(page: ft.Page):
    page.title = "MaterialPicker"
    page.padding = 20

    selected = ft.Text("#ff9800")
    swatch = ft.Container(width=40, height=40, bgcolor="#ff9800", border_radius=6)

    def on_color_change(e: ft.ControlEvent):
        selected.value = e.data
        swatch.bgcolor = e.data
        page.update()

    picker = MaterialPicker(
        picker_color="#ff9800",
        on_color_change=on_color_change,
    )

    page.add(
        ft.Row(
            spacing=12,
            controls=[swatch, selected],
        ),
        picker,
    )


ft.run(main)
