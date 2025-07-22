import time

import flet as ft


def main(page: ft.Page):
    global dic
    dic = {}
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def change():
        while True:
            third_circle.border = ft.border.all(40, "#FFBFC1")
            page.update()
            time.sleep(0.6)
            second_circle.border = ft.border.all(40, "#FFDDDF")
            page.update()
            time.sleep(0.6)
            third_circle.border = ft.border.all(0, "#FFBFC1")
            second_circle.border = ft.border.all(80, "#FFDDDF")
            page.update()
            time.sleep(0.6)
            second_circle.border = ft.border.all(0, "#FFDDDF")
            page.update()
            time.sleep(0.6)

    inner_circle = ft.Container(
        animate=ft.Animation(600, "easeInOut"),
        width=50,
        height=50,
        border_radius=1000,
        bgcolor="#FF4445",
    )
    second_circle = ft.Container(
        animate=ft.Animation(600, "easeInOut"),
        border_radius=1000,
        border=ft.border.all(0, "#FFDDDF"),
    )
    third_circle = ft.Container(
        animate=ft.Animation(600, "easeInOut"),
        border_radius=1000,
        border=ft.border.all(0, "#FFBFC1"),
    )
    third_circle.content = second_circle
    second_circle.content = inner_circle
    page.add(third_circle)
    change()


ft.app(target=main)
