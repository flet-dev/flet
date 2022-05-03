import time

import flet
from flet import Container, ElevatedButton, Text


def main(page):

    c = Container(content=Text("A"))

    def btn_click(e):
        c.content = Text(str(time.time()))
        page.update()

    page.add(c, ElevatedButton("Replace!", on_click=btn_click))


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
