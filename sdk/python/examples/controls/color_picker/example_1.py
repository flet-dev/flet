import flet as ft
from flet_color_picker import ColorPicker


def main(page: ft.Page):
    page.title = "ColorPicker"
    page.padding = 20

    selected = ft.Text("#ff0000")
    swatch = ft.Container(width=40, height=40, bgcolor="#ff0000", border_radius=6)

    def on_color_change(e: ft.ControlEvent):
        selected.value = e.data
        swatch.bgcolor = e.data
        page.update()

    picker = ColorPicker(
        picker_color="#ff0000",
        color_picker_width=320,
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
