import json
import logging
from datetime import datetime
from msilib.schema import Icon
from time import sleep
from turtle import width

import flet
from flet import Column, ElevatedButton, Image, Page, Row, Text, Theme
from flet.stack import Stack

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Images Example"
    page.theme_mode = "light"
    page.padding = 50
    page.update()

    images = Row(expand=1, wrap=False, auto_scroll=True)

    page.add(images)

    for i in range(0, 30):
        images.controls.append(
            Image(
                src=f"https://picsum.photos/100/100?{i}",
                width=100,
                height=100,
                fit="none",
                repeat="noRepeat",
            )
        )
    page.update()


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
