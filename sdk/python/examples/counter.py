import flet
from flet import Button, Stack, Textbox
import logging

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
        Stack(
            horizontal=True,
            controls=[
                Button("-", on_click=on_click, data="-"),
                txt_number,
                Button("+", on_click=on_click, data="+"),
            ],
        )
    )


flet.app("counter", target=main)
