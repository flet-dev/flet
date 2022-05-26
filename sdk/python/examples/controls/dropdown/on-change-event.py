import flet
from flet import Dropdown, Page, Text, dropdown


def main(page: Page):
    def dropdown_changed(e):
        t.value = f"Dropdown changed to {dd.value}"
        page.update()

    t = Text()
    dd = Dropdown(
        on_change=dropdown_changed,
        options=[
            dropdown.Option("Red"),
            dropdown.Option("Green"),
            dropdown.Option("Blue"),
        ],
        width=200,
    )
    page.add(dd, t)


flet.app(target=main)
