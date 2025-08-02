import flet
from flet import Page, Text


def main(page: Page):
    page.add(Text(f"Initial route: {page.route}"))


flet.app(target=main, view=flet.AppView.WEB_BROWSER)
