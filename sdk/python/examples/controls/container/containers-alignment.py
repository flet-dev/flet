import flet
from flet import Container, ElevatedButton, Page, Row, alignment, colors


def main(page: Page):
    page.title = "Containers with different alignments"

    c1 = Container(
        content=ElevatedButton("Center"),
        bgcolor=colors.AMBER,
        padding=15,
        alignment=alignment.center,
        width=150,
        height=150,
    )

    c2 = Container(
        content=ElevatedButton("Top left"),
        bgcolor=colors.AMBER,
        padding=15,
        alignment=alignment.top_left,
        width=150,
        height=150,
    )

    c3 = Container(
        content=ElevatedButton("-0.5, -0.5"),
        bgcolor=colors.AMBER,
        padding=15,
        alignment=alignment.Alignment(-0.5, -0.5),
        width=150,
        height=150,
    )

    r = Row([c1, c2, c3])
    page.add(r)


flet.app(target=main)
