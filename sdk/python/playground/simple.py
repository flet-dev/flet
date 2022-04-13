import logging
from datetime import datetime

import flet
from flet import ElevatedButton, Text
from flet.page import Page

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Simple Example"
    page.theme_mode = "dark"
    page.update()

    def on_click(e):
        page.add(Text(f"Line {datetime.now()}"))

    page.add(
        ElevatedButton("Click me!", on_click=on_click),
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
