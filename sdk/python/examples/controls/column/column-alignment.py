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

    def column_with_alignment(align):
        return Column(
            [
                Text(align, size=16),
                Container(
                    content=Column(items(3), alignment=align),
                    bgcolor=colors.AMBER_100,
                    height=400,
                ),
            ]
        )

    page.add(
        Row(
            [
                column_with_alignment("start"),
                column_with_alignment("center"),
                column_with_alignment("end"),
                column_with_alignment("spaceBetween"),
                column_with_alignment("spaceAround"),
                column_with_alignment("spaceEvenly"),
            ],
            spacing=30,
            alignment="start",
        )
    )


flet.app(target=main)
