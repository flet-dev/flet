import flet
from flet import ElevatedButton, Page


def main(page: Page):
    page.title = "Elevated button"
    page.add(ElevatedButton("Hello, world!"))


flet.app(target=main)
