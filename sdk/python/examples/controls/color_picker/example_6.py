import flet as ft
from flet_color_picker import MultipleChoiceBlockPicker


def main(page: ft.Page):
    page.title = "MultipleChoiceBlockPicker"
    page.padding = 20

    selected = ft.Text("#03a9f4, #4caf50")
    swatch = ft.Container(width=40, height=40, bgcolor="#03a9f4", border_radius=6)

    def on_colors_change(e: ft.ControlEvent):
        colors = e.data or []
        selected.value = ", ".join(colors)
        if colors:
            swatch.bgcolor = colors[0]
        page.update()

    picker = MultipleChoiceBlockPicker(
        picker_colors=["#03a9f4", "#4caf50"],
        available_colors=[
            "#f44336",
            "#e91e63",
            "#9c27b0",
            "#3f51b5",
            "#2196f3",
            "#03a9f4",
            "#009688",
            "#4caf50",
            "#ff9800",
            "#795548",
        ],
        on_colors_change=on_colors_change,
    )

    page.add(
        ft.Row(
            spacing=12,
            controls=[swatch, selected],
        ),
        picker,
    )


ft.run(main)
