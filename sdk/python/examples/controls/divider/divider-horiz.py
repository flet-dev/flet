import flet
from flet import Column, Container, Divider, Page, alignment, colors


def main(page: Page):

    page.add(
        Column(
            [
                Container(
                    bgcolor=colors.AMBER,
                    alignment=alignment.center,
                    expand=True,
                ),
                Divider(),
                Container(bgcolor=colors.PINK, alignment=alignment.center, expand=True),
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
    )


flet.app(target=main)
