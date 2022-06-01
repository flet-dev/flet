import flet
from flet import Checkbox, ElevatedButton, Text


def main(page):
    def button_clicked(e):
        t.value = f"Checkboxes values are:  {c1.value}, {c2.value}, {c3.value}, {c4.value}, {c5.value}."
        page.update()

    t = Text()
    c1 = Checkbox(label="Unchecked by default checkbox", value=False)
    c2 = Checkbox(label="Undefined by default tristate checkbox", tristate=True)
    c3 = Checkbox(label="Checked by default checkbox", value=True)
    c4 = Checkbox(label="Disabled checkbox", disabled=True)
    c5 = Checkbox(
        label="Checkbox with rendered label_position='left'", label_position="left"
    )
    b = ElevatedButton(text="Submit", on_click=button_clicked)
    page.add(c1, c2, c3, c4, c5, b, t)


flet.app(target=main)
