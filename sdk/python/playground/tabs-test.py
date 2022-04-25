import logging
from time import sleep

import flet
from flet import Icon, Page, Tab, Tabs, Text, alignment, icons
from flet.container import Container

logging.basicConfig(level=logging.DEBUG)


def main(page: Page):
    page.title = "Tabs example"

    t = Tabs(
        value="tab2",
        animation_duration=300,
        tabs=[
            Tab(
                key="tab1",
                text="Tab 1",
                content=Container(
                    content=Text("This is Tab 1"), alignment=alignment.center
                ),
            ),
            Tab(
                key="tab2",
                tab_content=Icon(icons.MESSAGE),
                content=Text("This is Tab 2"),
            ),
            Tab(
                key="tab3",
                text="Tab 3",
                icon=icons.IRON,
                content=Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    page.add(t)

    sleep(3)
    t.value = "tab3"
    page.update()
    sleep(3)
    t.value = "tab1"
    page.update()
    sleep(3)
    t.value = "tab2"
    t.tabs.pop(0)
    t.tabs[1].content = Text("Blah blah blah")
    page.update()
    sleep(3)
    t.tabs.clear()
    page.update()
    sleep(3)
    t.tabs.append(
        Tab(
            key="tab4",
            text="Tab 4",
            icon=icons.LOCK,
            content=Text("This is Tab 4"),
        )
    )
    t.tabs.append(
        Tab(
            key="tab5",
            text="Tab 5",
            icon=icons.SIP_SHARP,
            content=Text("This is Tab 5"),
        )
    )
    page.update()


flet.app(
    name="test1",
    port=8550,
    target=main,
    view=flet.WEB_BROWSER,
)
