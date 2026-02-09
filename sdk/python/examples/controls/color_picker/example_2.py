import flet as ft
from flet_color_picker import HueRingPicker


def main(page: ft.Page):
    page.title = "HueRingPicker"
    page.padding = 20

    def on_color_change(e: ft.ControlEvent):
        print(f"color: {e.data}")

    picker = HueRingPicker(
        color="#00ff00",
        hue_ring_stroke_width=20,
        picker_area_border_radius=ft.BorderRadius.all(5),
        on_color_change=on_color_change,
    )

    page.add(picker)


ft.run(main)
