import logging
from cmath import exp
from datetime import datetime
from time import sleep
from tkinter import W

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
    icons,
    padding,
)
from flet.border_radius import BorderRadius
from flet.checkbox import Checkbox
from flet.container import Container
from flet.icon import Icon
from flet.list_view import ListView
from flet.radio import Radio
from flet.radio_group import RadioGroup
from flet.stack import Stack
from flet.switch import Switch
from flet.textfield import TextField

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "TextField Examples"
    page.theme_mode = "light"
    page.padding = padding.all(20)

    results = Column(scroll="always", height=100)

    page.add(
        Column(
            [
                Text("Outlined TextField", style="headlineMedium"),
                TextField(),
                Text(
                    "Outlined TextField with Label, Hint and Helper text",
                    style="headlineSmall",
                ),
                TextField(
                    label="Full name",
                    hint_text="Enter your full name",
                    helper_text="Hint text is visible when TextField is empty and focused",
                ),
                Text(
                    "Underlined, filled and multiline TextField",
                    style="headlineSmall",
                ),
                TextField(
                    label="Comments",
                    helper_text="Tell something about us",
                    border="underline",
                    filled=True,
                    min_lines=1,
                ),
                Text(
                    "Login with email/password",
                    style="headlineSmall",
                ),
                TextField(
                    label="Email",
                    prefix_icon=icons.EMAIL,
                    border="underline",
                    keyboard_type="email",
                    filled=True,
                ),
                TextField(
                    label="Password",
                    prefix_icon=icons.PASSWORD_SHARP,
                    border="underline",
                    password=True,
                    can_reveal_password=True,
                    filled=True,
                ),
            ],
            scroll="always",
            expand=1,
            width=600,
        ),
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
