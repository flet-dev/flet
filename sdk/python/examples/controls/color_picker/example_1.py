import flet as ft
from flet_color_picker import ColorLabelType, ColorPicker, PaletteType


def main(page: ft.Page):
    page.title = "ColorPicker"
    page.padding = 20

    selected = ft.Text("#ff0000")
    swatch = ft.Container(width=40, height=40, bgcolor="#ff0000", border_radius=6)

    def on_color_change(e: ft.ControlEvent):
        selected.value = e.data
        swatch.bgcolor = e.data
        print(f"color: {e.data}")
        page.update()

    def on_history_change(e: ft.ControlEvent):
        # e.data is a list of hex strings
        print(f"history: {e.data}")

    def on_hsv_color_change(e: ft.ControlEvent):
        # e.data is a dict with alpha, hue, saturation, value
        # print(f"hsv: {e.data}")
        print("hsv: ", e.control.picker_hsv_color)

    picker = ColorPicker(
        picker_color="#ff0000",
        picker_hsv_color={
            "alpha": 1.0,
            "hue": 200.0,
            "saturation": 0.9,
            "value": 0.8,
        },
        display_thumb_color=False,
        enable_alpha=False,
        hex_input_bar=False,
        label_text_style=ft.TextStyle(color=ft.Colors.BLUE, size=14, italic=True),
        color_history=[
            "#ff0000",
            "#00ff00",
            "#0000ff",
            "#ffff00",
            "#00ffff",
            "#ff00ff",
        ],
        color_picker_width=420,
        on_color_change=on_color_change,
        on_history_change=on_history_change,
        on_hsv_color_change=on_hsv_color_change,
        label_types=[
            ColorLabelType.HEX,
            # ColorLabelType.RGB,
            ColorLabelType.HSV,
            ColorLabelType.HSL,
        ],
        palette_type=PaletteType.HSV_WITH_HUE,
        picker_area_border_radius=ft.BorderRadius.all(20),
        picker_area_height_percent=0.3,
    )

    page.add(
        ft.Row(
            spacing=12,
            controls=[swatch, selected],
        ),
        picker,
    )


ft.run(main)
