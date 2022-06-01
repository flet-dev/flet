import flet
from flet import Slider, Text


def main(page):
    def slider_changed(e):
        t.value = f"Slider changed to {e.control.value}"
        page.update()

    t = Text()
    page.add(
        Text("Slider with 'on_change' event:"),
        Slider(
            min=0, max=100, divisions=10, label="{value}%", on_change=slider_changed
        ),
        t,
    )


flet.app(target=main)
