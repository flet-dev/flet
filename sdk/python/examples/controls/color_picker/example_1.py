import flet as ft
from flet_color_picker import ColorLabelType, ColorPicker


def main(page: ft.Page):
    page.title = "ColorPicker"
    page.padding = 20

    def on_color_change(e: ft.ControlEvent):
        print(f"color: {e.data}")

    def on_history_change(e: ft.ControlEvent):
        # e.data is a list of hex strings
        print(f"history: {e.data}")

    def on_hsv_color_change(e: ft.ControlEvent):
        print("hsv: ", e.control.picker_hsv_color)

    picker = ColorPicker(
        # picker_color="#ff0000",
        picker_hsv_color={
            "alpha": 1.0,
            "hue": 60.0,
            "saturation": 1.0,
            "value": 1.0,
        },
        color_history=[
            "#ff0000",
            "#00ff00",
            "#0000ff",
            "#ffff00",
            "#00ffff",
            "#ff00ff",
        ],
        on_color_change=on_color_change,
        on_history_change=on_history_change,
        on_hsv_color_change=on_hsv_color_change,
        label_types=[
            ColorLabelType.HEX,
            ColorLabelType.RGB,
        ],
        picker_area_border_radius=ft.BorderRadius.all(20),
    )

    page.add(picker)


ft.run(main)
