import logging
from time import sleep

import flet
from flet import Icon, Page, Tab, Tabs, Text, alignment, icons
from flet.container import Container

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Tabs example"

    t = Tabs(
        selected_index=1,
        animation_duration=300,
        tabs=[
            Tab(
                text="Tab 1",
                content=Container(
                    content=Text("This is Tab 1"), alignment=alignment.center
                ),
            ),
            Tab(
                tab_content=Icon(icons.MESSAGE),
                content=Text("This is Tab 2"),
            ),
            Tab(
                text="Tab 3",
                icon=icons.IRON,
                content=Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    page.add(t)

    sleep(7)
    t.selected_index = 2
    page.update()
    sleep(3)
    t.selected_index = 0
    page.update()
    sleep(3)
    t.selected_index = 1
    t.tabs.pop(0)
    t.tabs[1].content = Text("Blah blah blah")
    page.update()
    sleep(3)
    t.tabs.clear()
    page.update()
    sleep(3)
    t.tabs.append(
        Tab(
            text="Tab 4",
            icon=icons.LOCK,
            content=Text("This is Tab 4"),
        )
    )
    t.tabs.append(
        Tab(
            text="Tab 5",
            icon=icons.SIP_SHARP,
            content=Text("This is Tab 5"),
        )
    )
    page.update()


flet.app(target=main)
