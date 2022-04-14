import logging
from datetime import datetime

import flet
from flet import ElevatedButton, Text
from flet.page import Page

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Simple Example"
    page.theme_mode = "light"
    page.padding = 50
    page.spacing = 30
    page.vertical_alignment = "center"
    page.horizontal_alignment = "end"
    page.update()

    def on_click1(e):
        page.add(Text(f"Line {datetime.now()}"))

    def on_click2(e):
        page.content.pop()
        page.update()

    page.add(
        ElevatedButton("Click me!", on_click=on_click1),
        ElevatedButton("Remove last control", on_click=on_click2),
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
