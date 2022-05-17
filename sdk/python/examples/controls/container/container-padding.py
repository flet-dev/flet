import flet
from flet import Container, ElevatedButton, Page, Row, colors, padding


def main(page: Page):
    page.title = "Containers with different padding"

    c1 = Container(
        content=ElevatedButton("container_1"),
        bgcolor=colors.AMBER,
        padding=padding.all(10),
        width=150,
        height=150,
    )

    c2 = Container(
        content=ElevatedButton("container_2"),
        bgcolor=colors.AMBER,
        padding=padding.all(20),
        width=150,
        height=150,
    )

    c3 = Container(
        content=ElevatedButton("container_3"),
        bgcolor=colors.AMBER,
        padding=padding.symmetric(horizontal=10),
        width=150,
        height=150,
    )

    c4 = Container(
        content=ElevatedButton("container_4"),
        bgcolor=colors.AMBER,
        padding=padding.only(left=10),
        width=150,
        height=150,
    )

    r = Row([c1, c2, c3, c4])
    page.add(r)


flet.app(target=main)
