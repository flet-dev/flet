import time

import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def change():
        start = -1
        while True:
            if start == -1:
                bubble1.height = 50
                page.update()
                start = 1
            else:
                time.sleep(0.5)
                bubble4.height = 20
                bubble1.height = 60
                page.update()
            time.sleep(0.5)
            bubble1.height = 20
            bubble2.height = 60
            page.update()
            time.sleep(0.5)
            bubble2.height = 20
            bubble3.height = 60
            page.update()
            time.sleep(0.5)
            bubble3.height = 20
            bubble4.height = 60
            page.update()

    bubble1 = ft.Container(
        animate=ft.Animation(600, "bounceOut"),
        width=20,
        height=60,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble2 = ft.Container(
        animate=ft.Animation(600, "bounceOut"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble3 = ft.Container(
        animate=ft.Animation(600, "bounceOut"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble4 = ft.Container(
        animate=ft.Animation(600, "bounceOut"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    loading = ft.Row(alignment="center", controls=[bubble1, bubble2, bubble3, bubble4])
    page.add(loading)
    change()


ft.app(target=main)
