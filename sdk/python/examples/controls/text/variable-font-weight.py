import flet as ft


def main(page: ft.Page):
    page.fonts = {
        "RobotoSlab": "https://github.com/google/fonts/raw/main/apache/robotoslab/RobotoSlab%5Bwght%5D.ttf"
    }

    def handle_slider_change(e):
        text.weight = f"w{int(e.control.value)}"  # noqa
        text.update()

    page.add(
        text := ft.Text(
            "This is rendered with Roboto Slab",
            size=30,
            font_family="RobotoSlab",
            weight=ft.FontWeight.W_100,
        ),
        ft.Slider(
            min=100,
            max=900,
            divisions=8,
            label="Weight = {value}",
            width=500,
            on_change=handle_slider_change,
        ),
    )


ft.run(main)
