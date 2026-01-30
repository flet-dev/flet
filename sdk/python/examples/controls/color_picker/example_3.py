import flet as ft
from flet_color_picker import ColorLabelType, ColorModel, SlidePicker


def main(page: ft.Page):
    page.title = "SlidePicker"
    page.padding = 20

    selected = ft.Text("#0000ff")
    swatch = ft.Container(width=40, height=40, bgcolor="#0000ff", border_radius=6)

    def on_color_change(e: ft.ControlEvent):
        selected.value = e.data
        swatch.bgcolor = e.data
        print(f"color: {e.data}")
        page.update()

    picker = SlidePicker(
        picker_color="#0000ff",
        color_model=ColorModel.RGB,
        display_thumb_color=False,
        enable_alpha=True,
        indicator_alignment_begin=ft.Alignment(-1, 0),
        indicator_alignment_end=ft.Alignment(1, 0),
        indicator_border_radius=ft.BorderRadius.all(20),
        indicator_size=ft.Size(300, 46),
        label_text_style=ft.TextStyle(size=12, color=ft.Colors.RED),
        label_types=[
            ColorLabelType.RGB,
        ],
        show_indicator=True,
        show_label=False,
        show_params=False,
        show_slider_text=True,
        slider_size=ft.Size(340, 36),
        slider_text_style=ft.TextStyle(size=12, color=ft.Colors.PINK),
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
