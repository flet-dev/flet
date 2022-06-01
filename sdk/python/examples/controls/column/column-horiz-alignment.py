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

    def column_with_horiz_alignment(align):
        return Column(
            [
                Text(align, size=16),
                Container(
                    content=Column(
                        items(3), alignment="start", horizontal_alignment=align
                    ),
                    bgcolor=colors.AMBER_100,
                    width=100,
                ),
            ]
        )

    page.add(
        Row(
            [
                column_with_horiz_alignment("start"),
                column_with_horiz_alignment("center"),
                column_with_horiz_alignment("end"),
            ],
            spacing=30,
            alignment="start",
        )
    )


flet.app(target=main)
