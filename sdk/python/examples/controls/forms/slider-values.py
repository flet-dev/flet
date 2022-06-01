import flet
from flet import Slider, Text


def main(page):
    page.add(
        Text("Slider with value:"),
        Slider(value=0.3),
        Text("Slider with a custom range and label:"),
        Slider(min=0, max=100, divisions=10, label="{value}%"),
    )


flet.app(target=main)
