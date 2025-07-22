import time

import flet as ft


def main(page: ft.Page):
    global dic
    dic = {}
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def animate(i, j):
        global dic
        time.sleep(0.6)
        exec(f"dic['bubble{i}'].width=20;")
        exec(f"dic['bubble{i}'].height=20;")
        exec(f"dic['bubble{j}'].width=25;")
        exec(f"dic['bubble{j}'].height=25;")
        if dic[f"bubble{j}"].bgcolor == "#B932FD":
            dic[f"bubble{j}"].bgcolor = "white"
        else:
            dic[f"bubble{j}"].bgcolor = "#B932FD"
        page.update()

    def change():
        start = -1
        prev = 16
        while True:
            li = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
            for i in li:
                animate(prev, i)
                prev = i

    def make_bubble(j):
        global dic
        for i in range(1, j + 1):
            dic[f"bubble{i}"] = ft.Container(
                animate=ft.Animation(600, "easeInOut"),
                width=20,
                height=20,
                border_radius=100,
                bgcolor="white",
            )

    make_bubble(16)
    loading = ft.Column(
        alignment="center",
        controls=[
            ft.Row(
                alignment="center",
                controls=[
                    dic["bubble1"],
                    dic["bubble2"],
                    dic["bubble3"],
                    dic["bubble4"],
                ],
            ),
            ft.Row(
                alignment="center",
                controls=[
                    dic["bubble5"],
                    dic["bubble6"],
                    dic["bubble7"],
                    dic["bubble8"],
                ],
            ),
            ft.Row(
                alignment="center",
                controls=[
                    dic["bubble9"],
                    dic["bubble10"],
                    dic["bubble11"],
                    dic["bubble12"],
                ],
            ),
            ft.Row(
                alignment="center",
                controls=[
                    dic["bubble13"],
                    dic["bubble14"],
                    dic["bubble15"],
                    dic["bubble16"],
                ],
            ),
        ],
    )
    page.add(loading)
    change()


ft.app(target=main)
