import time

import flet as ft


def main(page: ft.Page):
    global dic
    dic = {}
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    angel_ = 0

    def change():
        angel_1 = 1
        angel_2 = 1
        count = 0
        while True:
            count += 1
            angel_1 += 1
            angel_2 += -1
            if count >= 3:
                while 1:
                    count -= 1
                    angel_1 += -1
                    angel_2 += 1
                    container1.rotate = ft.Rotate(
                        angle=angel_1, alignment=ft.alignment.center
                    )
                    container2.rotate = ft.Rotate(
                        angle=angel_2, alignment=ft.alignment.center
                    )
                    page.update()
                    time.sleep(0.6)
                    if count <= 0:
                        break
            container1.rotate = ft.Rotate(angle=angel_1, alignment=ft.alignment.center)
            container2.rotate = ft.Rotate(angle=angel_2, alignment=ft.alignment.center)
            page.update()
            time.sleep(0.6)

    container1 = ft.Container(
        animate=ft.Animation(600, "easeInOut"),
        animate_rotation=ft.Animation(600, "easeInOut"),
        height=220,
        width=220,
        border=ft.border.all(5, "red"),
        bgcolor="white",
        rotate=ft.Rotate(angle=1, alignment=ft.alignment.center),
    )
    container2 = ft.Container(
        animate=ft.Animation(600, "easeInOut"),
        animate_rotation=ft.Animation(600, "easeInOut"),
        height=220,
        width=220,
        border=ft.border.all(5, "black"),
        bgcolor="white",
        rotate=ft.Rotate(angle=1, alignment=ft.alignment.center),
    )
    page.add(ft.Stack(controls=[container1, container2]))
    change()


ft.app(target=main)
