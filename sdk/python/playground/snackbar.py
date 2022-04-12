import logging

import flet
from flet import ElevatedButton, SnackBar

logging.basicConfig(level=logging.DEBUG)


class Data:
    def __init__(self) -> None:
        self.counter = 0


d = Data()


def main(page):
    page.title = "SnackBar Example"
    page.update()

    sb = SnackBar(content=f"Hello, world!")

    def on_click(e):
        sb.content = f"Hello, world: {d.counter}"
        sb.open = True
        d.counter += 1
        page.update()

    page.add(ElevatedButton("Open SnackBar", on_click=on_click), sb)


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
