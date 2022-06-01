from time import sleep

import flet
from flet import Page, Text


def main(page: Page):
    txt1 = Text("Line 1")
    txt2 = Text("Line 2")
    txt3 = Text("Line 3")

    page.add(txt1, txt2, txt3)

    sleep(4)

    txt2.visible = False
    # page.controls.pop(1)
    page.update()


flet.app(name="test1", port=8550, target=main, view=flet.FLET_APP)
