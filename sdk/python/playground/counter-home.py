import logging

import flet
from flet import IconButton, Page, Row, TextField, icons
from flet.progress_bar import ProgressBar


def main(page: Page):
    page.title = "Flet counter example"
    page.vertical_alignment = "center"
    page.splash = ProgressBar()

    txt_number = TextField(value="0", text_align="right", width=100)

    def minus_click(e):
        txt_number.value = int(txt_number.value) - 1
        page.update()

    def add_click(e):
        txt_number.value = int(txt_number.value) + 1
        page.update()

    page.add(
        Row(
            [
                IconButton(icons.REMOVE, on_click=minus_click),
                txt_number,
                IconButton(icons.ADD, on_click=add_click),
            ],
            alignment="center",
        )
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
