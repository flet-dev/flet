import time

import flet as ft


def main(page: ft.Page):
    global dic
    dic = {}
    page.bgcolor = "black"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    global def_
    def_ = 0

    def animate(init, i):
        dic[f"container{i}"].alignment = ft.alignment.Alignment(0, init)

    def animate_squeeze(i):
        pass

    def change():
        while True:
            global def_
            if def_ == 0:
                init = 1
                while True:
                    init -= 0.1
                    animate(init, 0)
                    animate(init, 1)
                    animate(init, 2)
                    page.update()
                    if init <= -0.9:
                        break
                def_ = 1
            else:
                init = -1
                while True:
                    init += 0.1
                    animate(init, 0)
                    animate(init, 1)
                    animate(init, 2)
                    page.update()
                    if init >= 0.9:
                        animate_squeeze(0)
                        animate_squeeze(1)
                        animate_squeeze(2)
                        break
                def_ = 0
            time.sleep(0.5)

    dic["container0"] = ft.Container(
        animate=ft.animation.Animation(300, "easeInOut"),
        height=140,
        width=30,
        bgcolor="black",
        alignment=ft.alignment.Alignment(0, 1),
    )
    ball = ft.Container(height=25, width=25, bgcolor="white", border_radius=40)
    dic["container1"] = ft.Container(
        animate=ft.animation.Animation(500, "easeInOut"),
        height=140,
        width=30,
        bgcolor="black",
        alignment=ft.alignment.Alignment(0, 1),
    )
    ball1 = ft.Container(height=25, width=25, bgcolor="white", border_radius=40)
    dic["container2"] = ft.Container(
        animate=ft.animation.Animation(700, "easeInOut"),
        height=140,
        width=30,
        bgcolor="black",
        alignment=ft.alignment.Alignment(0, 1),
    )
    ball2 = ft.Container(height=25, width=25, bgcolor="white", border_radius=40)
    dic["container0"].content = ball
    dic["container1"].content = ball1
    dic["container2"].content = ball2
    text_ = ft.Text(
        "Loading...",
        size=35,
        color=ft.Colors.WHITE,
        weight=ft.FontWeight.BOLD,
    )
    page.add(
        ft.Column(
            alignment="center",
            controls=[
                ft.Row(
                    alignment="center",
                    controls=[dic["container0"], dic["container1"], dic["container2"]],
                ),
                ft.Row(alignment="center", controls=[text_]),
            ],
        )
    )
    change()


ft.app(target=main)
