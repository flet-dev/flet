import flet
from flet import Image, Page, Row, Stack, Text


def main(page: Page):
    st = Stack(
        [
            Image(
                src=f"https://picsum.photos/300/300",
                width=300,
                height=300,
                fit="contain",
            ),
            Row(
                [
                    Text(
                        "Image title",
                        color="white",
                        size=40,
                        weight="bold",
                        opacity=0.5,
                    )
                ],
                alignment="center",
            ),
        ],
        width=300,
        height=300,
    )

    page.add(st)


flet.app(target=main)
