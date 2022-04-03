import logging

import flet
from flet import Button, Column, Row, Textbox
from flet.expanded import Expanded

logging.basicConfig(level=logging.DEBUG)


def main(page):
    page.title = "Counter"
    page.update()

    def on_click(e):
        try:
            count = int(txt_number.value)

            txt_number.error_message = ""

            if e.data == "+":
                txt_number.value = count + 1

            elif e.data == "-":
                txt_number.value = count - 1

        except ValueError:
            txt_number.error_message = "Please enter a number"

        page.update()

    txt_number = Textbox(value="0", align="right")

    page.add(
        Expanded(
            Row(
                controls=[
                    Button("-", on_click=on_click, data="-"),
                    Expanded(txt_number),
                    Expanded(Textbox(label="Another textbox")),
                    Button("+", on_click=on_click, data="+"),
                ],
            )
        ),
        Expanded(),
    )


flet.app(name="test1", port=8550, target=main)
