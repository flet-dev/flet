from doctest import Example

import flet
from flet import (
    Column,
    Container,
    Divider,
    Page,
    Row,
    Text,
    VerticalDivider,
    alignment,
    colors,
)


def main(page: Page):

    page.add(
        Row(
            [
                Column(
                    [
                        Container(
                            bgcolor=colors.AMBER,
                            alignment=alignment.center,
                            expand=True,
                        ),
                        Divider(),
                        Container(
                            bgcolor=colors.PINK, alignment=alignment.center, expand=True
                        ),
                        Divider(height=1, color="white"),
                        Container(
                            bgcolor=colors.BLUE_300,
                            alignment=alignment.center,
                            expand=True,
                        ),
                        Divider(height=9, thickness=3),
                        Container(
                            bgcolor=colors.DEEP_PURPLE_200,
                            alignment=alignment.center,
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                ),
                Row(
                    [
                        Container(
                            bgcolor=colors.ORANGE_300,
                            alignment=alignment.center,
                            expand=True,
                        ),
                        VerticalDivider(),
                        Container(
                            bgcolor=colors.BROWN_400,
                            alignment=alignment.center,
                            expand=True,
                        ),
                        VerticalDivider(width=1, color="white"),
                        Container(
                            bgcolor=colors.BLUE_300,
                            alignment=alignment.center,
                            expand=True,
                        ),
                        VerticalDivider(width=9, thickness=3),
                        Container(
                            bgcolor=colors.GREEN_300,
                            alignment=alignment.center,
                            expand=True,
                        ),
                    ],
                    spacing=0,
                    expand=True,
                ),
            ],
            expand=True,
        )
    )


flet.app(target=main, view=flet.WEB_BROWSER)
