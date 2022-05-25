import flet
from flet import Card, Column, Container, Icon, ListTile, Row, Text, TextButton, icons


def main(page):
    page.title = "Card Example"
    page.add(
        Card(
            content=Container(
                content=Column(
                    [
                        ListTile(
                            leading=Icon(icons.ALBUM),
                            title=Text("The Enchanted Nightingale"),
                            subtitle=Text(
                                "Music by Julie Gable. Lyrics by Sidney Stein."
                            ),
                        ),
                        Row(
                            [TextButton("Buy tickets"), TextButton("Listen")],
                            alignment="end",
                        ),
                    ]
                ),
                width=400,
                padding=10,
            )
        )
    )


flet.app(target=main)
