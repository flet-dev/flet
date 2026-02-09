import flet as ft
from flet_color_picker import ColorModel, SlidePicker


def main(page: ft.Page):
    page.title = "SlidePicker"
    page.padding = 20

    def on_color_change(e: ft.ControlEvent):
        print(f"color: {e.data}")

    picker = SlidePicker(
        color="#0000ff",
        color_model=ColorModel.RGB,
        indicator_border_radius=ft.BorderRadius.all(5),
        on_color_change=on_color_change,
    )

    page.add(picker)


ft.run(main)
