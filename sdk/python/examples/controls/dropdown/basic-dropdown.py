import flet
from flet import Dropdown, ElevatedButton, Page, Text, dropdown


def main(page: Page):
    def button_clicked(e):
        t.value = f"Dropdown value is:  {dd.value}"
        page.update()

    t = Text()
    b = ElevatedButton(text="Submit", on_click=button_clicked)
    dd = Dropdown(
        width=100,
        options=[
            dropdown.Option("Red"),
            dropdown.Option("Green"),
            dropdown.Option("Blue"),
        ],
    )
    page.add(dd, b, t)


flet.app(target=main)
