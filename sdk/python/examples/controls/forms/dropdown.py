import logging
import os

import flet
from flet import Dropdown, ElevatedButton, dropdown

logging.basicConfig(level=logging.INFO)


def main(page):
    dd = Dropdown(
        options=[
            dropdown.Option("a", "Item A"),
            dropdown.Option("b", "Item B"),
            dropdown.Option("c", "Item C"),
        ]
    )

    def btn2_click(e):
        dd.options.append(dropdown.Option("d", "Item D"))
        page.update()

    def btn3_click(e):
        dd.options[1].text = "Item Blah Blah Blah"
        page.update()

    btn2 = ElevatedButton("Add new item!", on_click=btn2_click)
    btn3 = ElevatedButton("Change second item", on_click=btn3_click)

    page.add(dd, btn2, btn3)


flet.app(target=main)
