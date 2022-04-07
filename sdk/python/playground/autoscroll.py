import logging

import flet
from flet import Button, Image, Stack, Text

logging.basicConfig(level=logging.DEBUG)

page = flet.page("autoscroll", update=False, no_window=True, permissions="")
# page.theme_primary_color = "green"
# page.gap = 100
# page.padding = 100
# page.update()

st = Stack(scroll_y=True, auto_scroll=True)

scroll_box = Stack(
    height="400", width="100%", bgcolor="#f0f0f0", vertical_align="end", controls=[st]
)


def add_click(e):
    page.i += 1
    st.controls.append(
        Stack(
            horizontal=True,
            vertical_align="center",
            controls=[
                Image(
                    src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
                    width=30,
                    height=30,
                    border_radius=15,
                    fit="contain",
                ),
                Text(f"Line {page.i}"),
            ],
        )
    )
    st.update()


page.add(scroll_box, Button("Add line", primary=True, focused=True, on_click=add_click))

for i in range(0, 10):
    st.controls.append(Text(f"Line {i}"))
    st.update()

page.i = i

input()
