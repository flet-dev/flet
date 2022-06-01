import flet
from flet import Container, Icon, Page, Tab, Tabs, Text, alignment, icons


def main(page: Page):

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
                tab_content=Icon(icons.SEARCH),
                content=Text("This is Tab 2"),
            ),
            Tab(
                text="Tab 3",
                icon=icons.SETTINGS,
                content=Text("This is Tab 3"),
            ),
        ],
        expand=1,
    )

    page.add(t)


flet.app(target=main)
