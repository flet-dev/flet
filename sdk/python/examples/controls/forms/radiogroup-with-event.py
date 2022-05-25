import flet
from flet import Column, Radio, RadioGroup, Text


def main(page):
    def radiogroup_changed(e):
        t.value = f"Your favorite color is:  {e.control.value}"
        page.update()

    t = Text()
    cg = RadioGroup(
        content=Column(
            [
                Radio(value="red", label="Red"),
                Radio(value="green", label="Green"),
                Radio(value="blue", label="Blue"),
            ]
        ),
        on_change=radiogroup_changed,
    )

    page.add(Text("Select your favorite color:"), cg, t)


flet.app(target=main)
