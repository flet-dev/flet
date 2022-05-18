from time import sleep

import flet
from flet import Column, Page, ProgressBar, Text


def main(page: Page):
    pb = ProgressBar(width=400)

    page.add(
        Text("Linear progress indicator", style="headlineSmall"),
        Column([Text("Doing something..."), pb]),
        Text("Indeterminate progress bar", style="headlineSmall"),
        ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
    )

    for i in range(0, 101):
        pb.value = i * 0.01
        sleep(0.1)
        page.update()


flet.app(target=main)
