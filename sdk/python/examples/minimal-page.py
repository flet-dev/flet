from time import sleep

import flet
from flet import Button, Stack, Text, Textbox

page = flet.page(no_window=True)

txt1 = Text("Text A")
txt2 = Text("Text B")
tb1 = Textbox(label="Your name", value="John")
btn1 = Button("Click me!", on_click=lambda e: print("I'm clicked!", tb1.value))


def btn2_click(e):
    tb1.value = tb1.value + "A"
    tb1.label = tb1.label + "B"
    page.update()


btn2 = Button("Append", on_click=btn2_click)

st1 = Stack(
    horizontal=False,
    controls=[txt1, txt2],
)
page.add(st1, btn1, btn2)

sleep(3)

for i in range(1, 10):
    # txt1.value = f"Hello, world - {i}"
    st1.controls.append(Text(f"Hello, world - {i}"))
    if len(st1.controls) > 5:
        st1.controls.pop(0)
    page.update()
    # sleep(1)

st1.controls.append(tb1)
page.update()

sleep(5)

# st1.bgcolor = "red"
btn1.text = "Boo!"
page.update()

sleep(2)

# update text
st1.controls[1].value = "Line 2"
st1.controls[3].value = "Line 4"
page.update()

# input()
