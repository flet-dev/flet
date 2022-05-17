import flet
from flet import IconButton, Page, Row, icons


def main(page: Page):
    page.title = "Icon buttons"
    page.add(
        Row(
            [
                IconButton(
                    icon=icons.PAUSE_CIRCLE_FILLED_ROUNDED,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Pause record",
                ),
                IconButton(
                    icon=icons.DELETE_FOREVER_ROUNDED,
                    icon_color="pink600",
                    icon_size=40,
                    tooltip="Delete record",
                ),
            ]
        ),
    )


flet.app(target=main)
