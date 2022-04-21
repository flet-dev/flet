import logging

import flet
from flet import ElevatedButton, SnackBar, Text

logging.basicConfig(level=logging.DEBUG)


class Data:
    def __init__(self) -> None:
        self.counter = 0


d = Data()


def main(page):
    page.title = "SnackBar Example"
    page.update()

    def action_click(e):
        print("I've got my snacks!")

    page.snack_bar = SnackBar(
        content=Text("Hello, world!"),
        remove_current_snackbar=True,
        action="Alright!",
        on_action=action_click,
    )

    def on_click(e):
        page.snack_bar.content.value = f"Hello, world: {d.counter}"
        page.snack_bar.open = True
        d.counter += 1
        page.update()

    page.add(ElevatedButton("Open SnackBar", on_click=on_click))


flet.app(name="test1", port=8550, target=main, view=flet.FLET_APP)
