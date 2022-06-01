import logging
from cmath import exp
from datetime import datetime
from time import sleep

import flet
from flet import (
    Column,
    Dropdown,
    ElevatedButton,
    Image,
    Page,
    Row,
    Text,
    Theme,
    border,
    border_radius,
    dropdown,
    padding,
)
from flet.border_radius import BorderRadius
from flet.checkbox import Checkbox
from flet.container import Container
from flet.icon import Icon
from flet.list_view import ListView
from flet.radio import Radio
from flet.radio_group import RadioGroup
from flet.slider import Slider
from flet.stack import Stack
from flet.switch import Switch

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Form Example"
    page.theme_mode = "light"
    page.padding = padding.all(20)

    results = Column(scroll="always", height=100)

    checkboxes = Column(
        [
            Checkbox(value=True),
            Checkbox(label="A simple checkbox with a label"),
            Checkbox(label="Checkbox with tristate", tristate=True),
            Checkbox(label="Disabled checkbox", disabled=True),
            Checkbox(label="Label on the left", label_position="left"),
        ]
    )

    switches = Column(
        [
            Switch(value=True),
            Switch(value=False),
            Switch(label="Switch with a label"),
            Switch(label="Disabled switch", disabled=True),
            Switch(label="Label on the left", label_position="left"),
        ]
    )

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
        results.controls.append(Text(f"Selected value: {rg1.value}"))
        page.update()

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

    dd = Dropdown(
        options=[
            dropdown.Option("a", "Item A"),
            dropdown.Option("b", "Item B"),
            dropdown.Option("c", "Item C"),
        ],
        value="b",
        content_padding=padding.all(5),
        height=35,
    )

    dd1 = Dropdown(
        options=[
            dropdown.Option("r", "Red"),
            dropdown.Option("g", "Green"),
            dropdown.Option("b", "Blue"),
        ]
    )
    dd2 = Dropdown(
        options=[
            dropdown.Option("1", "One"),
            dropdown.Option("2", "Two"),
            dropdown.Option("3", "Three"),
        ],
        label="My favorite number",
        icon="format_size",
        hint_text="Choose your favorite color",
        helper_text="You can choose only one color",
        counter_text="0 colors selected",
        prefix_icon="color_lens",
        suffix_text="...is your color",
    )

    page.add(
        Column(
            [
                Text("Checkboxes", style="headlineMedium"),
                checkboxes,
                Text("Switches", style="headlineMedium"),
                switches,
                Text("Radio", style="headlineMedium"),
                rg,
                Text("Radio with on_change", style="headlineMedium"),
                rg1,
                Container(
                    content=results,
                    padding=10,
                    border=border.all(1, "black12"),
                    border_radius=border_radius.all(10),
                    bgcolor="black12",
                ),
                Text("Dropdown with pre-selected value", style="headlineMedium"),
                dd,
                Text("Dropdown", style="headlineMedium"),
                dd1,
                Text("Dropdown with all decoration", style="headlineMedium"),
                dd2,
                Text("Slider", style="headlineMedium"),
                Slider(value=0.5),
                Slider(min=0, max=100, divisions=10, value=30, label="{value}%"),
            ],
            scroll="always",
            expand=1,
        ),
    )


flet.app(target=main)
