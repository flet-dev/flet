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


def main(page: Page):
    def items(count):
        items = []
        for i in range(1, count + 1):
            items.append(
                Container(
                    content=Text(value=i),
                    alignment=alignment.center,
                    width=50,
                    height=50,
                    bgcolor=colors.AMBER,
                    border_radius=border_radius.all(5),
                )
            )
        return items

    def gap_slider_change(e):
        row.spacing = int(e.control.value)
        row.update()

    gap_slider = Slider(
        min=0,
        max=50,
        divisions=50,
        value=0,
        label="{value}",
        on_change=gap_slider_change,
    )

    row = Row(spacing=0, controls=items(10))

    page.add(Column([Text("Spacing between items"), gap_slider]), row)


flet.app(target=main)
