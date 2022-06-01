import flet
from flet import (
    Column,
    Container,
    Icon,
    OutlinedButton,
    Page,
    Row,
    Text,
    icons,
    padding,
)


def main(page: Page):
    page.title = "Outlined buttons with custom content"
    page.add(
        OutlinedButton(
            width=150,
            content=Row(
                [
                    Icon(name=icons.FAVORITE, color="pink"),
                    Icon(name=icons.AUDIOTRACK, color="green"),
                    Icon(name=icons.BEACH_ACCESS, color="blue"),
                ],
                alignment="spaceAround",
            ),
        ),
        OutlinedButton(
            content=Container(
                content=Column(
                    [
                        Text(value="Compound button", size=20),
                        Text(value="This is secondary text"),
                    ],
                    alignment="center",
                    spacing=5,
                ),
                padding=padding.all(10),
            ),
        ),
    )


flet.app(target=main)
