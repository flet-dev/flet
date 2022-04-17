import logging
from ctypes import alignment
from datetime import datetime
from time import sleep

import flet
from flet import Page, alignment, padding
from flet.container import Container
from flet.text import Text

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Images Example"
    page.theme_mode = "light"
    page.padding = padding.all(100)
    page.update()

    c = Container(
        content=Text("Hello, world!"),
        margin=10,
        padding=10,
        alignment=alignment.Alignment(0.5, -0.5),
        bgcolor="amber",
        width=300,
        height=300,
    )

    page.add(c)


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
