import flet
from flet import Icon, Page, Row, colors, icons


def main(page: Page):
    page.add(
        Row(
            [
                Icon(name=icons.FAVORITE, color=colors.PINK),
                Icon(name=icons.AUDIOTRACK, color=colors.GREEN_400, size=30),
                Icon(name=icons.BEACH_ACCESS, color=colors.BLUE, size=50),
                Icon(name="settings", color="#c1c1c1"),
            ]
        )
    )


flet.app(target=main)
