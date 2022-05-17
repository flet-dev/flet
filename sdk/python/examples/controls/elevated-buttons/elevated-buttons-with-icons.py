import flet
from flet import ElevatedButton, Page


def main(page: Page):
    page.title = "Elevated buttons with icons"
    page.add(
        ElevatedButton("Button with icon", icon="chair_outlined"),
        ElevatedButton(
            "Button with colorful icon",
            icon="park_rounded",
            icon_color="green400",
        ),
    )


flet.app(target=main)
