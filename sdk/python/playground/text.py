import json
import logging
from datetime import datetime
from msilib.schema import Icon

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
    page.update()

    page.add(
        ListView(
            [
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
                Text("Size 10", size=10),
                Text("Size 30", size=20, color="pink600"),
                Text("Size 50", size=50, color="white", bgcolor="orange800"),
            ],
            expand=1,
        )
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
