import flet
from flet import Card, Container, Text


def main(page):
    page.title = "Card Examples"
    # page.theme_mode = "dark"
    page.add(
        Card(
            content=Container(
                content=Text("A regular card with padded content"), padding=10
            ),
            margin=0,
        ),
        Card(
            content=Container(content=Text("A card with custom elevation"), padding=10),
            elevation=5,
        ),
    )


flet.app(name="test1", port=8550, target=main, view=flet.WEB_BROWSER)
