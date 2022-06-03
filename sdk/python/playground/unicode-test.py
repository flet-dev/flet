import flet
from flet import Page, Text


def main(page: Page):
    page.add(Text("Testing ä ë ï ö ü"))


flet.app(target=main, view=flet.WEB_BROWSER)
