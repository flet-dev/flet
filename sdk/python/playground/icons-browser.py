import logging
import os
from datetime import datetime
from time import sleep
from turtle import onclick

import flet
from flet import (
    Column,
    Container,
    GridView,
    Icon,
    IconButton,
    OutlinedButton,
    Page,
    Row,
    SnackBar,
    Text,
    TextButton,
    TextField,
    alignment,
    border_radius,
    colors,
    icons,
    padding,
)

# logging.basicConfig(level=logging.DEBUG)

# fetch all icon constants from icons.py module
icons_list = []
list_started = False
for key, value in vars(icons).items():
    if key == "TEN_K":
        list_started = True
    if list_started:
        icons_list.append(value)

os.environ["FLET_WS_MAX_MESSAGE_SIZE"] = "8000000"


def main(page: Page):
    page.title = "Flet icons browser"
    page.theme_mode = "light"

    search_txt = TextField(
        expand=1,
        hint_text="Enter keyword and press search button",
        autofocus=True,
        on_submit=lambda e: display_icons(e.control.value),
    )
    search_results = GridView(
        expand=1,
        runs_count=10,
        max_extent=150,
        spacing=5,
        run_spacing=5,
        child_aspect_ratio=1,
    )
    status_bar = Text()

    def copy_to_clipboard(e):
        icon_key = e.control.data
        print("Copy to clipboard:", icon_key)
        page.clipboard = e.control.data
        page.snack_bar = SnackBar(Text(f"Copied {icon_key}"), open=True)
        page.update()

    def display_icons(search_term: str):

        # clean search results
        search_results.clean()

        # add matching icons
        for i in range(0, len(icons_list)):
            if search_term != "" and search_term in icons_list[i]:
                icon_name = icons_list[i]
                icon_key = f"icons.{icon_name.upper()}"
                search_results.controls.append(
                    TextButton(
                        content=Container(
                            content=Column(
                                [
                                    Icon(name=icon_name, size=30),
                                    Text(
                                        value=icon_name,
                                        size=12,
                                        width=100,
                                        no_wrap=True,
                                        text_align="center",
                                        color=colors.ON_SURFACE_VARIANT,
                                    ),
                                ],
                                spacing=5,
                                alignment="center",
                                horizontal_alignment="center",
                            ),
                            alignment=alignment.center,
                        ),
                        tooltip=f"{icon_key}\nClick to copy to a clipboard",
                        on_click=copy_to_clipboard,
                        data=icon_key,
                    )
                )

                # update page on every 500 icons added
                if i > 0 and i % 500 == 0:
                    status_bar.value = f"Icons found: {len(search_results.controls)}"
                    page.update()
        status_bar.value = f"Icons found: {len(search_results.controls)}"
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
        status_bar,
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
