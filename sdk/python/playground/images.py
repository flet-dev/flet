import logging
from datetime import datetime
from time import sleep

import flet
from flet import Column, ElevatedButton, Image, Page, Row, Text, Theme
from flet.stack import Stack

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Images Example"
    page.theme_mode = "light"
    page.padding = 50
    page.update()

    img = Image(
        src=f"/icons/Icon-512.png",
        width=100,
        height=100,
        fit="contain",
    )
    images = Row(expand=1, wrap=True, scroll="always")

    page.add(img, images)

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


flet.app(name="test1", port=8550, target=main, view=flet.FLET_APP)
