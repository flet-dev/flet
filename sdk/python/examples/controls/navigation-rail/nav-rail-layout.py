import logging
from time import sleep

import flet
from flet import (
    Column,
    FloatingActionButton,
    Icon,
    NavigationRail,
    NavigationRailDestination,
    Page,
    Row,
    Text,
    icons,
)
from flet.divider import Divider
from flet.vertical_divider import VerticalDivider

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    def fab_click(e):
        rail.selected_index = 2
        select_page()
        page.update()

    pages = [
        Text("First", visible=False),
        Text("Second!", visible=False),
        Text("Settings", visible=False),
    ]

    def select_page():
        print(f"Selected index: {rail.selected_index}")
        for index, p in enumerate(pages):
            p.visible = True if index == rail.selected_index else False
        page.update()

    def dest_change(e):
        select_page()

    rail = NavigationRail(
        selected_index=0,
        label_type="all",
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=FloatingActionButton(icon=icons.CREATE, text="Add", on_click=fab_click),
        # trailing=Text("Something"),
        group_alignment=-0.9,
        destinations=[
            NavigationRailDestination(
                icon=icons.FAVORITE_BORDER, selected_icon=icons.FAVORITE, label="First"
            ),
            NavigationRailDestination(
                icon_content=Icon(icons.BOOKMARK_BORDER),
                selected_icon_content=Icon(icons.BOOKMARK),
                label="Second",
            ),
            NavigationRailDestination(
                icon=icons.SETTINGS, label_content=Text("Settings")
            ),
        ],
        on_change=dest_change,
    )

    select_page()

    page.add(
        Row(
            [
                rail,
                VerticalDivider(width=1),
                Column(pages, alignment="start", expand=True),
            ],
            expand=True,
        )
    )


flet.app(target=main)
