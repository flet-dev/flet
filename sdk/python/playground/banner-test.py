import logging

import flet
from flet import Banner, ElevatedButton, Icon, Text, TextButton, colors, icons

logging.basicConfig(level=logging.DEBUG)


class Data:
    def __init__(self) -> None:
        self.counter = 0


d = Data()


def main(page):
    page.title = "SnackBar Example"
    page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

    page.banner = Banner(
        bgcolor=colors.AMBER_100,
        leading=Icon(icons.WARNING_AMBER_ROUNDED, color=colors.AMBER, size=40),
        content=Text(
            "Oops, there were some errors while trying to delete the file. What would you like me to do?"
        ),
        actions=[
            TextButton("Retry", on_click=close_banner),
            TextButton("Ignore", on_click=close_banner),
            TextButton("Cancel", on_click=close_banner),
        ],
    )

    def show_banner_click(e):
        page.banner.open = True
        page.update()

    page.add(ElevatedButton("Show Banner", on_click=show_banner_click))


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
