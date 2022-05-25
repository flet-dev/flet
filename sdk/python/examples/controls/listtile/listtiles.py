import logging

import flet
from flet import (
    Card,
    Column,
    Container,
    Icon,
    Image,
    ListTile,
    PopupMenuButton,
    PopupMenuItem,
    Text,
    icons,
    padding,
)

logging.basicConfig(level=logging.DEBUG)


def main(page):
    page.title = "ListTile Examples"
    # page.theme_mode = "dark"
    page.add(
        Card(
            content=Container(
                width=500,
                content=Column(
                    [
                        ListTile(
                            title=Text("One-line list tile"),
                        ),
                        ListTile(title=Text("One-line dense list tile"), dense=True),
                        ListTile(
                            leading=Icon(icons.SETTINGS),
                            title=Text("One-line selected list tile"),
                            selected=True,
                        ),
                        ListTile(
                            leading=Image(src="/icons/icon-192.png", fit="contain"),
                            title=Text("One-line with leading control"),
                        ),
                        ListTile(
                            title=Text("One-line with trailing control"),
                            trailing=PopupMenuButton(
                                icon=icons.MORE_VERT,
                                items=[
                                    PopupMenuItem(text="Item 1"),
                                    PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ListTile(
                            leading=Icon(icons.ALBUM),
                            title=Text("One-line with leading and trailing controls"),
                            trailing=PopupMenuButton(
                                icon=icons.MORE_VERT,
                                items=[
                                    PopupMenuItem(text="Item 1"),
                                    PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                        ListTile(
                            leading=Icon(icons.SNOOZE),
                            title=Text("Two-line with leading and trailing controls"),
                            subtitle=Text("Here is a second title."),
                            trailing=PopupMenuButton(
                                icon=icons.MORE_VERT,
                                items=[
                                    PopupMenuItem(text="Item 1"),
                                    PopupMenuItem(text="Item 2"),
                                ],
                            ),
                        ),
                    ],
                    spacing=0,
                ),
                padding=padding.symmetric(vertical=10),
            )
        )
    )


flet.app(target=main)
