import flet
from flet import Slider, Text


def main(page):
    page.add(
        Text("Default slider:"),
        Slider(),
        Text("Default disabled slider:"),
        Slider(disabled=True),
    )


flet.app(target=main)
