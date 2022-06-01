import flet
from flet import (
    Column,
    Container,
    Page,
    Row,
    Slider,
    Text,
    alignment,
    border_radius,
    colors,
)

HEIGHT = 400


def main(page: Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                Container(
                    content=Text(value=i),
                    alignment=alignment.center,
                    width=30,
                    height=30,
                    bgcolor=colors.AMBER,
                    border_radius=border_radius.all(5),
                )
            )
        return items

    def slider_change(e):
        col.height = float(e.control.value)
        col.update()

    width_slider = Slider(
        min=0,
        max=HEIGHT,
        divisions=20,
        value=HEIGHT,
        label="{value}",
        width=500,
        on_change=slider_change,
    )

    col = Column(
        wrap=True,
        spacing=10,
        run_spacing=10,
        controls=items(10),
        height=HEIGHT,
    )

    page.add(
        Column(
            [
                Text(
                    "Change the column height to see how child items wrap onto multiple columns:"
                ),
                width_slider,
            ]
        ),
        Container(content=col, bgcolor=colors.AMBER_100),
    )


flet.app(target=main)
