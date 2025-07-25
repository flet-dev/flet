import asyncio

import flet as ft

name = "ProgressBar Example"


def example():
    class Example(ft.Column):
        def __init__(self):
            super().__init__()
            self.t = ft.Text(value="Click the button...")
            self.pb = ft.ProgressBar(width=400, value=0)
            self.b = ft.FilledTonalButton("Start", on_click=self.button_clicked)
            self.controls = [
                ft.Text(
                    "Linear progress indicator",
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                ),
                ft.Column([self.t, self.pb]),
                ft.Text(
                    "Indeterminate progress bar",
                    theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                ),
                ft.ProgressBar(width=400, color="amber", bgcolor="#eeeeee"),
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
                self.pb.value = i * 0.01
                await asyncio.sleep(0.1)
                if not self.pb_mounted:
                    break
                self.pb.update()
            self.t.value = "Click the button..."
            self.b.disabled = False

        # happens when example is added to the page (when user chooses the ProgressBar control from the grid)
        def did_mount(self):
            self.pb_mounted = True

        # happens when example is removed from the page (when user chooses different control group on the navigation rail)
        def will_unmount(self):
            self.pb_mounted = False

    pb_example = Example()

    return pb_example
