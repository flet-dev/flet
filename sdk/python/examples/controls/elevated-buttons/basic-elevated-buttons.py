import flet
from flet import ElevatedButton, Page


def main(page: Page):
    page.title = "Basic elevated buttons"
    page.add(
        ElevatedButton(text="Elevated button"),
        ElevatedButton("Disabled button", disabled=True),
    )


flet.app(target=main)
