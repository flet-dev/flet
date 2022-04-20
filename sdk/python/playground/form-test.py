import logging
from datetime import datetime
from time import sleep

import flet
from flet import Column, ElevatedButton, Image, Page, Row, Text, Theme, padding
from flet.checkbox import Checkbox
from flet.radio import Radio
from flet.radio_group import RadioGroup
from flet.stack import Stack

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Form Example"
    page.theme_mode = "light"
    page.padding = padding.all(20)

    rg = RadioGroup(
        content=Column(
            [
                Radio(value="red", label="Red color"),
                Radio(value="green", label="Green color"),
                Radio(value="blue", label="Blue color"),
            ]
        )
    )

    def rg1_on_change(e):
        page.add(Text(f"Selected value: {rg1.value}"))

    rg1 = RadioGroup(
        content=Row(
            [
                Radio(value="one", label="One"),
                Radio(value="two", label="Two"),
                Radio(value="three", label="Three"),
            ]
        ),
        value="two",
        on_change=rg1_on_change,
    )

    page.add(
        Text("Checkboxes", style="headlineMedium"),
        Checkbox(value=True),
        Checkbox(label="A simple checkbox with a label"),
        Checkbox(label="Checkbox with tristate", tristate=True),
        Checkbox(label="Disabled checkbox", disabled=True),
        Checkbox(label="Label on the left", label_position="left"),
        Text("Radio", style="headlineMedium"),
        rg,
        Text("Radio with on_change", style="headlineMedium"),
        rg1,
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
