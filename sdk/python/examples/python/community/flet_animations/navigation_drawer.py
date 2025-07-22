import time

import flet as ft


def main(page: ft.Page):
    global dic
    dic = {}
    page.alignment = "center"
    page.bgcolor = "#2A282A"
    angel_ = 0
    global def_
    def_ = 0

    def change():
        global def_
        if def_ == 0:
            def_ = 1
            line2.width = 0
            page.update()
            time.sleep(0.2)
            column = ft.Stack(controls=[line1, line3])
            container.content = column
            page.update()
            time.sleep(0.1)
            container.border_radius = 100
            line1.rotate = ft.Rotate(angle=0.81, alignment=ft.alignment.center)
            line3.rotate = ft.Rotate(angle=-0.81, alignment=ft.alignment.center)
            page.update()
        else:
            def_ = 0
            container.border_radius = 10
            line1.rotate = ft.Rotate(angle=0, alignment=ft.alignment.center)
            line3.rotate = ft.Rotate(angle=0, alignment=ft.alignment.center)
            page.update()
            time.sleep(0.1)
            column = ft.Column(
                controls=[line1, line2, line3], alignment="center", spacing=4.6
            )
            container.content = column
            page.update()
            time.sleep(0.2)
            line2.width = 30
            page.update()

    container = ft.Container(
        animate=ft.Animation(100, "easeInOut"),
        height=50,
        width=50,
        bgcolor="#FFFFFF",
        border_radius=10,
        alignment=ft.alignment.center,
        on_click=lambda i: [change()],
    )
    line1 = ft.Container(
        animate=ft.Animation(100, "easeInOut"),
        animate_rotation=ft.Animation(100, "easeInOut"),
        width=30,
        height=5,
        bgcolor="#5B7CF4",
        border_radius=5,
        rotate=ft.Rotate(angle=0, alignment=ft.alignment.center),
    )
    line2 = ft.Container(
        animate=ft.Animation(100, "easeInOut"),
        width=30,
        height=5,
        bgcolor="#5B7CF4",
        border_radius=5,
    )
    line3 = ft.Container(
        animate=ft.Animation(100, "easeInOut"),
        animate_rotation=ft.Animation(100, "easeInOut"),
        width=30,
        height=5,
        bgcolor="#5B7CF4",
        border_radius=5,
        rotate=ft.Rotate(angle=-0, alignment=ft.alignment.center),
    )
    column = ft.Column(controls=[line1, line2, line3], alignment="center", spacing=4.6)
    container.content = column
    page.add(container)


ft.app(target=main)
