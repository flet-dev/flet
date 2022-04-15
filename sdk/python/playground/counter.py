import logging

import flet
from flet import Column, Row, Text, TextField
from flet.elevated_button import ElevatedButton

logging.basicConfig(level=logging.DEBUG)


def main(page):
    page.title = "Counter"
    page.padding = 10
    page.update()

    def on_click(e):
        try:
            count = int(txt_number.value)

            txt_number.error_text = ""

            if e.data == "+":
                txt_number.value = count + 1

            elif e.data == "-":
                txt_number.value = count - 1

            result.value = f"Clicked: {e.data}"

        except ValueError:
            txt_number.error_text = "Please enter a number"

        page.update()

    txt_number = TextField(value="0", text_align="right", expand=1)
    result = Text()

    page.add(
        Row(
            controls=[
                ElevatedButton("-", on_click=on_click, data="-"),
                txt_number,
                ElevatedButton("+", on_click=on_click, height=50, data="+"),
                Column(controls=[result]),
            ],
            width=400,
            height=50,
        ),
        Column(controls=[Text("Just some text")]),
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
