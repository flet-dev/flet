import flet as ft
from flet_color_picker import BlockPicker


def main(page: ft.Page):
    page.title = "BlockPicker"
    page.padding = 20

    selected = ft.Text("#9c27b0")
    swatch = ft.Container(width=40, height=40, bgcolor="#9c27b0", border_radius=6)

    def on_color_change(e: ft.ControlEvent):
        selected.value = e.data
        swatch.bgcolor = e.data
        page.update()

    picker = BlockPicker(
        picker_color="#9c27b0",
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
