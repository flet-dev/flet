import flet
from flet import Column, Container, Page, Row, Text, alignment, colors


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
                    bgcolor=colors.AMBER_500,
                )
            )
        return items

    def row_with_vertical_alignment(align):
        return Column(
            [
                Text(align, size=16),
                Container(
                    content=Row(items(3), vertical_alignment=align),
                    bgcolor=colors.AMBER_100,
                    height=150,
                ),
            ]
        )

    page.add(
        row_with_vertical_alignment("start"),
        row_with_vertical_alignment("center"),
        row_with_vertical_alignment("end"),
    )


flet.app(target=main)
