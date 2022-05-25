import flet
from flet import Column, ElevatedButton, Radio, RadioGroup, Text


def main(page):
    def button_clicked(e):
        t.value = f"Your favorite color is:  {cg.value}"
        page.update()

    t = Text()
    b = ElevatedButton(text="Submit", on_click=button_clicked)
    cg = RadioGroup(
        content=Column(
            [
                Radio(value="red", label="Red"),
                Radio(value="green", label="Green"),
                Radio(value="blue", label="Blue"),
            ]
        )
    )

    page.add(Text("Select your favorite color:"), cg, b, t)


flet.app(target=main)
