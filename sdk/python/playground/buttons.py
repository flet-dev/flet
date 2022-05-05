import logging
from datetime import datetime
from time import sleep

import flet
from flet import (
    Column,
    ElevatedButton,
    FloatingActionButton,
    Icon,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    Text,
    TextButton,
    icons,
)

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Buttons Example"
    page.theme_mode = "light"
    page.padding = 50

    page.add(
        Column(
            expand=1,
            scroll=True,
            controls=[
                Text("Elevated buttons", style="headlineMedium"),
                ElevatedButton("Normal button"),
                ElevatedButton("Disabled button", disabled=True),
                ElevatedButton(
                    "Button with icon and tooltip",
                    icon="chair_outlined",
                    tooltip="Hey, click me!",
                ),
                ElevatedButton(
                    "Button with colorful icon",
                    icon="park_rounded",
                    icon_color="green400",
                ),
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
                Text("Outlined buttons", style="headlineMedium"),
                OutlinedButton("Normal button"),
                OutlinedButton("Disabled button", disabled=True),
                OutlinedButton("Button with icon", icon="chair_outlined"),
                OutlinedButton(
                    "Button with colorful icon",
                    icon="park_rounded",
                    icon_color="green400",
                ),
                OutlinedButton(
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
                Text("Text buttons", style="headlineMedium"),
                TextButton("Normal button"),
                TextButton("Disabled button", disabled=True),
                TextButton("Button with icon", icon="chair_outlined"),
                TextButton(
                    "Button with colorful icon",
                    icon="park_rounded",
                    icon_color="green400",
                ),
                TextButton(
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
                Text("Icon buttons", style="headlineMedium"),
                Row(
                    [
                        IconButton(
                            icon="pause_circle_filled_sharp",
                            icon_color="blue400",
                            tooltip="Pause record",
                        ),
                        IconButton(
                            icon="delete_forever_rounded",
                            icon_color="pink600",
                            tooltip="Delete record",
                        ),
                        IconButton(
                            icon=icons.ANDROID,
                            icon_color="white",
                            bgcolor="blue",
                            tooltip="Beep... Beep... Beep...",
                        ),
                    ]
                ),
            ],
        )
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
