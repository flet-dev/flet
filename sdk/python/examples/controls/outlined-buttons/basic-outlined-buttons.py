import flet
from flet import OutlinedButton, Page


def main(page: Page):
    page.title = "Basic outlined buttons"
    page.add(
        OutlinedButton(text="Outlined button"),
        OutlinedButton("Disabled button", disabled=True),
    )


flet.app(target=main)
