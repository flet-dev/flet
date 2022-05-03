import json
import logging
from datetime import datetime
from msilib.schema import Icon
from time import sleep

from click import style

import flet
from flet import Column, ElevatedButton, ListView, Page, Row, Text, Theme
from flet.stack import Stack

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Text Examples"
    page.padding = 50
    page.spacing = 30
    page.vertical_alignment = "start"
    page.horizontal_alignment = "center"
    page.bgcolor = "blueGrey200"
    page.update()

    lv = ListView(expand=1, spacing=10, padding=20, auto_scroll=True)

    count = 1

    for i in range(0, 60):
        lv.controls.append(Text(f"Line {count}"))
        count += 1

    page.add(lv)

    for i in range(0, 60):
        sleep(1)
        lv.controls.append(Text(f"Line {count}"))
        count += 1
        page.update()


flet.app(name="test1", port=8550, target=main, view=flet.FLET_APP)
