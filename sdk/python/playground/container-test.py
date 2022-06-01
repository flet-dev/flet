import logging
from ctypes import alignment
from datetime import datetime
from time import sleep

import flet
from flet import Page, alignment, border, border_radius, colors, padding
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
        bgcolor=colors.AMBER,
        width=300,
        height=300,
        border=border.all(10, colors.PINK_600),
        border_radius=border_radius.all(30),
    )

    page.add(c)


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
