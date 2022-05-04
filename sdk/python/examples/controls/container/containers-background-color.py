import flet
from flet import Container, ElevatedButton, OutlinedButton, Page, colors


def main(page: Page):
    page.title = "Containers with background color"

    c1 = Container(
        content=ElevatedButton("Elevated Button in Container"),
        bgcolor=colors.YELLOW,
        padding=5,
    )

    c2 = Container(
        content=ElevatedButton(
            "Elevated Button with opacity=0.5 in Container", opacity=0.5
        ),
        bgcolor=colors.YELLOW,
        padding=5,
    )

    c3 = Container(
        content=OutlinedButton("Outlined Button in Container"),
        bgcolor=colors.YELLOW,
        padding=5,
    )
    page.add(c1, c2, c3)


flet.app(target=main)
