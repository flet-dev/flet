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

    st = Stack(
        [
            Image(
                src=f"https://picsum.photos/300/300",
                width=300,
                height=300,
                fit="contain",
            ),
            Row(
                [
                    Text(
                        "Image title",
                        color="white",
                        size=40,
                        weight="bold",
                        opacity=0.3,
                    )
                ],
                alignment="center",
            ),
        ],
        width=300,
        height=300,
    )

    page.add(st)


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
