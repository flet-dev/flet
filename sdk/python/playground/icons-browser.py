import logging
import os
from datetime import datetime
from time import sleep

import flet
from flet import (
    Column,
    Container,
    GridView,
    Icon,
    IconButton,
    ListView,
    OutlinedButton,
    Page,
    Row,
    Text,
    TextField,
    Theme,
    alignment,
    border,
    border_radius,
    colors,
    icons,
    padding,
)

# logging.basicConfig(level=logging.DEBUG)

# fetch all icon constants from icons.py module
icons_list = []
list_started = False
for name, value in vars(icons).items():
    if name == "TEN_K":
        list_started = True
    if list_started:
        icons_list.append(value)

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"


def main(page: Page):
    page.title = "Flet icons browser"

    search_txt = TextField(expand=1, hint_text="Enter keyword and press search button")
    # search_results = ListView(expand=1, wrap=True, scroll="always")
    # search_results = ListView(expand=1, spacing=2)
    search_results = GridView(
        expand=1, runs_count=10, max_extent=100, spacing=5, run_spacing=5
    )

    def display_icons(search_term: str):

        # clean search results
        search_results.controls.clear()
        page.update()

        # add matching icons
        for i in range(0, len(icons_list)):
            if search_term != "" and search_term in icons_list[i]:
                search_results.controls.append(
                    Container(
                        content=Column(
                            [
                                Icon(
                                    name=icons_list[i],
                                ),
                                Text(
                                    value=icons_list[i],
                                    size=10,
                                    width=100,
                                    # selectable=True,
                                    text_align="center",
                                    color=colors.BLACK87,
                                ),
                            ],
                            spacing=5,
                            alignment="center",
                            horizontal_alignment="center",
                        ),
                        alignment=alignment.center,
                        padding=padding.only(left=5, right=5),
                        # border=border.all(1, colors.BLACK26),
                        bgcolor="#f0f0f0",
                        border_radius=border_radius.all(3),
                    )
                )
        print("Icons found:", len(search_results.controls))
        if len(search_results.controls) == 0:
            search_results.controls.append(
                Text(f'No icons found with text "{search_term}".')
            )
        page.update()

    def search_click(e):
        display_icons(search_txt.value)

    page.add(
        Row([search_txt, IconButton(icon=icons.SEARCH, on_click=search_click)]),
        search_results,
    )


flet.app(name="test1", port=8550, target=main, view=flet.FLET_APP)
