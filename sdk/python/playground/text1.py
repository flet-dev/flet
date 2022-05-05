import flet
from flet import Text


def main(page):
    t = Text(
        value="This is a Text control sample",
        size=30,
        color="white",
        bgcolor="pink",
        weight="bold",
        italic=True,
    )
    page.add(t)


flet.app(target=main)
