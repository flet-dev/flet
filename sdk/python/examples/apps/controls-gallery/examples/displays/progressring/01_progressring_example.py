import asyncio

import flet as ft

name = "ProgressRing Example"


name = "ProgressBar Example"


def example():
    class Example(ft.Column):
        def __init__(self):
            super().__init__()
            self.t = ft.Text(value="Click the button...")
            self.pr = ft.ProgressRing(width=16, height=16, stroke_width=2)
            self.b = ft.FilledTonalButton("Start", on_click=self.button_clicked)
            self.controls = [
                ft.Text(
                    "Circular progress indicator",
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                ),
                ft.Row([self.pr, self.t]),
                ft.Text(
                    "Indeterminate cicrular progress",
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                ),
                ft.Column(
                    [ft.ProgressRing(), ft.Text("I'm going to run for ages...")],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.b,
            ]
            self.width = 400
            self.height = 400

        async def button_clicked(self, e):
            self.t.value = "Doing something..."
            self.t.update()
            self.b.disabled = True
            self.b.update()
            for i in range(0, 101):
                self.pr.value = i * 0.01
                await asyncio.sleep(0.1)
                if not self.pr_mounted:
                    break
                self.pr.update()
            self.t.value = "Click the button..."
            self.b.disabled = False

        # happens when example is added to the page (when user chooses the ProgressRing control from the grid)
        def did_mount(self):
            self.pr_mounted = True

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        def will_unmount(self):
            self.pr_mounted = False

    pr_example = Example()

    return pr_example
