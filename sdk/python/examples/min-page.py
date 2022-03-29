from time import sleep

import flet
from flet import Button, Stack, Text, Textbox

page = flet.page("page-1", no_window=True)

txt1 = Text("Text A")
# page.add(txt1)


st1 = Stack(
    controls=[
        Text("text 1"),
        Stack(
            controls=[
                Text("text 3"),
                Stack(
                    controls=[
                        Text("text 5"),
                        txt1,
                        Text("text 6"),
                    ]
                ),
                Text("text 4"),
            ]
        ),
        Text("text 2"),
    ]
)
page.add(st1)

sleep(3)

txt1.value = "Hello!"
page.update()

sleep(3)

txt1.value = "Bye!"
page.update()
