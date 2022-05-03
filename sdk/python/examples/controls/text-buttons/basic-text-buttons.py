import flet
from flet import Page, TextButton


def main(page: Page):
    page.title = "Basic text buttons"
    page.add(
        TextButton(text="Text button"),
        TextButton("Disabled button", disabled=True),
    )


flet.app(target=main)
