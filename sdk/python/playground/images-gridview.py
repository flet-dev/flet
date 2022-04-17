import logging
from datetime import datetime
from time import sleep

import flet
from flet import (
    Column,
    Container,
    ElevatedButton,
    Image,
    Page,
    Row,
    Text,
    Theme,
    border_radius,
)
from flet.grid_view import GridView
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
    images = GridView(
        expand=1, horizontal=False, runs_count=2, spacing=5, run_spacing=5
    )

    page.add(images)

    for i in range(0, 60):
        images.controls.append(
            Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit="none",
                repeat="noRepeat",
                border_radius=border_radius.all(10),
            )
        )
    page.update()


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
