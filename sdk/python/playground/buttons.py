import logging
from datetime import datetime
from time import sleep

import flet
from flet import ElevatedButton, Icon, Page, Row, Text

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Buttons Example"
    page.theme_mode = "light"
    page.padding = 50

    page.add(
        Text("Elevated buttons", style="headlineMedium"),
        ElevatedButton("Normal button"),
        ElevatedButton("Disabled button", disabled=True),
        ElevatedButton("Button with icon", icon="chair_outlined"),
        ElevatedButton(
            width=150,
            content=Row(
                [
                    Icon(name="favorite", color="pink"),
                    Icon(name="audiotrack", color="green"),
                    Icon(name="beach_access", color="blue"),
                ],
                alignment="spaceAround",
            ),
        ),
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
