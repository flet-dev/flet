from typing import Optional

import flet as ft


@ft.control(isolated=True)
class MyPanel(ft.Container):
    # control properties
    color: Optional[ft.ColorValue] = None
    greeting: str = "Hi"

    # called only once
    def build(self):
        print(self.page.platform)
        self.content = ft.Column(
            controls=[
                ft.Button(
                    f"Make {self.color.value}", on_click=self.on_change_color_click
                ),
                ft.Row(
                    [ft.Button(f"Say {self.greeting}!", on_click=self.on_say_click)]
                ),
            ]
        )

    def on_change_color_click(self, e):
        self.page.bgcolor = self.color
        self.page.update()

    def on_say_click(self, e):
        self.content.controls.append(ft.Text(self.greeting))


def main(page: ft.Page):
    page.controls.append(
        ft.Row(
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                MyPanel(color=ft.Colors.RED, width=200),
                MyPanel(color=ft.Colors.GREEN, greeting="whoops", width=200),
            ],
        )
    )


ft.run(main)
