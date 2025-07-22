import time

import flet as ft


def main(page: ft.Page):
    def on_enter():
        for i in range(100):
            time.sleep(0.001)
            pb.value += 0.01
            page.update()

    def on_exit():
        width = page.width
        for i in range(100):
            time.sleep(0.001)
            pb.value -= 0.01
            page.update()

    page.horizontal_alignment = page.vertical_alignment = "center"
    progress_bar = pb = ft.ProgressBar(
        width=185, value=0, color="amber", bgcolor="#eeeeee"
    )
    exp = ft.Column(
        alignment="center",
        controls=[
            ft.Row(
                alignment="center",
                controls=[
                    ft.Column(
                        controls=[
                            ft.GestureDetector(
                                content=ft.Text(
                                    value="Hello Everyone",
                                    style=ft.TextThemeStyle.HEADLINE_MEDIUM,
                                ),
                                on_enter=lambda i: [on_enter()],
                                on_exit=lambda i: [on_exit()],
                            ),
                            pb,
                        ]
                    )
                ],
            )
        ],
    )
    page.add(exp)


ft.app(target=main)
