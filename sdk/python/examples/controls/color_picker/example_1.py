import flet as ft
from flet_color_picker import ColorLabelType, ColorPicker, HsvColor, PaletteType


def main(page: ft.Page):
    page.title = "ColorPicker"
    page.padding = 20

    def on_color_change(e: ft.ControlEvent):
        print(f"color: {e.data}")

    def on_history_change(e: ft.ControlEvent):
        # e.data is a list of hex strings
        print(f"history: {e.data}")

    def on_hsv_color_change(e: ft.ControlEvent):
        print("hsv: ", e.control.hsv_color)

    picker = ColorPicker(
        # picker_color="#ff0000",
        hsv_color=HsvColor(alpha=1, hue=0, saturation=1, value=1),
        color_history=[
            "#ff0000",
            "#00ff00",
            "#0000ff",
            "#ffff00",
            "#00ffff",
            "#ff00ff",
        ],
        on_color_change=on_color_change,
        palette_type=PaletteType.RGB_WITH_GREEN,
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
