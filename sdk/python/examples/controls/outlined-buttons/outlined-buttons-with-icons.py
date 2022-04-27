import flet
from flet import OutlinedButton, Page


def main(page: Page):
    page.title = "Outlined buttons with icons"
    page.add(
        OutlinedButton("Button with icon", icon="chair_outlined"),
        OutlinedButton(
            "Button with colorful icon",
            icon="park_rounded",
            icon_color="green400",
        ),
    )


flet.app(target=main)
