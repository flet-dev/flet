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

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    def fab_click(e):
        rail.value = "third"
        page.update()

    rail = NavigationRail(
        value="Second",
        label_type="all",
        # extended=True,
        min_width=100,
        min_extended_width=400,
        leading=FloatingActionButton(icon=icons.CREATE, text="Add", on_click=fab_click),
        trailing=Text("Something"),
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
                key="third", icon=icons.STAR_BORDER, label_content=Text("Third")
            ),
        ],
        on_change=lambda e: print(f"Selected tab: {e.control.value}"),
    )

    page.add(Row([rail], expand=True))


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
