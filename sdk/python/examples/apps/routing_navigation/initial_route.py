import flet
from flet import Page, Text


def main(page: Page):
    page.add(Text(f"Initial route: {page.route}"))


flet.run(main)
