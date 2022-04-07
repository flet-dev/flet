import logging

import flet
from flet import Slider, Stack, Text

logging.basicConfig(level=logging.DEBUG)

with flet.page("horizontal-stack-wrapping") as page:

    bg_color = "#ddddee"
    page.horizontal_align = "stretch"

    def items(count):
        return [
            Text(
                value=i + 1,
                align="center",
                vertical_align="center",
                width=30,
                height=30,
                bgcolor="BlueMagenta10",
                color="white",
                padding=5,
            )
            for i in range(count)
        ]

    def wrap_slider_change(e):
        print("wrap_slider_change", e)
        width = int(e.control.value)
        wrap_stack.width = f"{width}%"
        wrap_stack.update()

    wrap_slider = Slider(
        "Change the stack width to see how child items wrap onto multiple rows:",
        min=0,
        max=100,
        step=1,
        value=100,
        show_value=True,
        value_format="{value}%",
        on_change=wrap_slider_change,
    )

    wrap_stack = Stack(
        horizontal=True, wrap=True, bgcolor=bg_color, gap=20, controls=items(10)
    )

    page.add(wrap_slider, wrap_stack)

    input()
