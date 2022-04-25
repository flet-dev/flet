import flet
from flet import Column, Container, ElevatedButton, Icon, Page, Row, Text, padding


def main(page: Page):
    page.title = "Elevated buttons with custom content"
    page.add(
        ElevatedButton(
            width=150,
            content=Row(
                [
                    Icon(name="favorite", color="pink"),
                    Icon(name="audiotrack", color="green"),
                    Icon(name="beach_access", color="blue"),
                ],
                alignment="spaceAround",
            ),
        ),
        ElevatedButton(
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
