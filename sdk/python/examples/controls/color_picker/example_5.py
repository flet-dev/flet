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
        available_colors=[
            "#f44336",
            "#e91e63",
            "#9c27b0",
            "#3f51b5",
            "#2196f3",
            "#009688",
            "#4caf50",
            "#ff9800",
            "#795548",
        ],
        use_in_show_dialog=True,
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
