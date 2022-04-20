import logging
from datetime import datetime
from time import sleep

import flet
from flet import Column, ElevatedButton, Image, Page, Row, Text, Theme, padding
from flet.checkbox import Checkbox
from flet.stack import Stack

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Form Example"
    page.theme_mode = "light"
    page.padding = padding.all(20)

    page.add(
        Checkbox(value=True),
        Checkbox(label="A simple checkbox with a label"),
        Checkbox(label="Checkbox with tristate", tristate=True),
        Checkbox(label="Disabled checkbox", disabled=True),
        Checkbox(label="Label on the left", label_position="left"),
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
