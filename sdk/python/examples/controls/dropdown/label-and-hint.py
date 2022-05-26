import flet
from flet import Dropdown, Page, dropdown


def main(page: Page):
    page.add(
        Dropdown(
            label="Color",
            hint_text="Choose your favourite color?",
            options=[
                dropdown.Option("Red"),
                dropdown.Option("Green"),
                dropdown.Option("Blue"),
            ],
            autofocus=True,
        )
    )


flet.app(target=main)
