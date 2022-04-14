import json
import logging
from datetime import datetime
from msilib.schema import Icon

from click import style

import flet
from flet import Column, ElevatedButton, Icon, Page, Row, Text, Theme
from flet.stack import Stack

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Text Examples"
    page.padding = 50
    page.spacing = 30
    page.vertical_alignment = "start"
    page.horizontal_alignment = "center"
    page.update()

    page.add(
        Text("Display Large", style="displayLarge"),
        Text("Display Medium", style="displayMedium"),
        Text("Display Small", style="displaySmall"),
        Text("Headline Large", style="headlineLarge"),
        Text("Headline Medium", style="headlineMedium"),
        Text("Headline Small", style="headlineSmall"),
        Text("Title Large", style="titleLarge"),
        Text("Title Medium", style="titleMedium"),
        Text("Title Small", style="titleSmall"),
        Text("Label Large", style="labelLarge"),
        Text("Label Medium", style="labelMedium"),
        Text("Label Small", style="labelSmall"),
        Text("Body Large", style="bodylLarge"),
        Text("Body Medium", style="bodyMedium"),
        Text("Body Small", style="bodySmall"),
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
