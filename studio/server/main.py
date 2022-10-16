import flet
from flet import Page, Text


def main(page: Page):
    page.add(
        Text("Hello, world!")
    )


flet.app(target=main, port=8550, view=flet.WEB_BROWSER)
