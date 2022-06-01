import flet
from flet import Page, TextButton


def main(page: Page):
    page.title = "Text buttons with icons"
    page.add(
        TextButton("Button with icon", icon="chair_outlined"),
        TextButton(
            "Button with colorful icon",
            icon="park_rounded",
            icon_color="green400",
        ),
    )


flet.app(target=main)
