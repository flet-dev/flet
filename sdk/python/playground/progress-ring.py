from time import sleep

import flet
from flet import Column, Page, ProgressRing, Row, Text


def main(page: Page):
    pr = ProgressRing(width=16, height=16, stroke_width=2)

    page.add(
        Text("Circular progress indicator", style="headlineSmall"),
        Row([pr, Text("Wait for the completion...")]),
        Text("Indeterminate cicrular progress", style="headlineSmall"),
        Column(
            [ProgressRing(), Text("I'm going to run for ages...")],
            horizontal_alignment="center",
        ),
    )

    for i in range(0, 101):
        pr.value = i * 0.01
        sleep(0.1)
        page.update()


flet.app(target=main)
