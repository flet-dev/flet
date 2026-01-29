import flet as ft
from flet_color_picker import SlidePicker


def main(page: ft.Page):
    page.title = "SlidePicker"
    page.padding = 20

    selected = ft.Text("#0000ff")
    swatch = ft.Container(width=40, height=40, bgcolor="#0000ff", border_radius=6)

    def on_color_change(e: ft.ControlEvent):
        selected.value = e.data
        swatch.bgcolor = e.data
        page.update()

    picker = SlidePicker(
        picker_color="#0000ff",
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
