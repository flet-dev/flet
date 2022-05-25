import flet
from flet import Container, Page, Row, VerticalDivider, alignment, colors


def main(page: Page):

    page.add(
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
        )
    )


flet.app(target=main)
