import logging

import flet
from flet import Button, Column, Row, Text, Textbox
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

            result.value = f"Clicked: {e.data}"

        except ValueError:
            txt_number.error_message = "Please enter a number"

        page.update()

    txt_number = Textbox(value="0", align="right")
    result = Text()

    page.add(
        Expanded(
            Row(
                controls=[
                    Button("-", on_click=on_click, data="-"),
                    Expanded(txt_number),
                    Expanded(Textbox(label="Another textbox")),
                    Button("+", on_click=on_click, data="+"),
                    Column(controls=[result]),
                ],
            )
        ),
        Expanded(Column(controls=[Text("Just some text")])),
    )


flet.app(name="test1", port=8550, target=main, view=flet.FLET_VIEW)
