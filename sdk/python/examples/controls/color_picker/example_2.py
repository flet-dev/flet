import flet as ft
from flet_color_picker import HueRingPicker


def main(page: ft.Page):
    page.title = "HueRingPicker"
    page.padding = 20

    selected = ft.Text("#00ff00")
    swatch = ft.Container(width=40, height=40, bgcolor="#00ff00", border_radius=6)

    def on_color_change(e: ft.ControlEvent):
        selected.value = e.data
        swatch.bgcolor = e.data
        page.update()

    picker = HueRingPicker(
        picker_color="#00ff00",
        on_color_change=on_color_change,
    )

    page.add(
        ft.Row(
            spacing=12,
            controls=[swatch, selected],
        ),
        picker,
    )


ft.app(main)
