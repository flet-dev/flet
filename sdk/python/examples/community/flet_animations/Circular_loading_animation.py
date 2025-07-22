import time

import flet as ft


def main(page: ft.Page):
    def animate(i, j):
        global \
            bubble1, \
            bubble2, \
            bubble3, \
            bubble4, \
            bubble5, \
            bubble6, \
            bubble7, \
            bubble8, \
            bubble9
        time.sleep(0.1)
        exec(f"bubble{i}.width=20;")
        exec(f"bubble{i}.height=20;")
        exec(f"bubble{j}.width=25;")
        exec(f"bubble{j}.height=25;")
        page.update()

    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    def change():
        start = -1
        while True:
            li = [1, 3, 5, 7, 8, 6, 4, 2]
            for i in range(len(li)):
                if i == 0:
                    animate(2, 1)
                else:
                    animate(li[i - 1], li[i])

    global \
        bubble1, \
        bubble2, \
        bubble3, \
        bubble4, \
        bubble5, \
        bubble6, \
        bubble7, \
        bubble8, \
        bubble9
    bubble1 = ft.Container(
        animate=ft.Animation(10, "linear"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble2 = ft.Container(
        animate=ft.Animation(10, "linear"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble3 = ft.Container(
        animate=ft.Animation(10, "linear"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble4 = ft.Container(
        animate=ft.Animation(10, "linear"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble5 = ft.Container(
        animate=ft.Animation(10, "linear"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble6 = ft.Container(
        animate=ft.Animation(10, "linear"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble7 = ft.Container(
        animate=ft.Animation(10, "linear"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    bubble8 = ft.Container(
        animate=ft.Animation(10, "linear"),
        width=20,
        height=20,
        border_radius=100,
        bgcolor="#B932FD",
    )
    loading = ft.Column(
        controls=[
            ft.Column(
                spacing=-1,
                controls=[
                    ft.Row(alignment="center", controls=[bubble1]),
                    ft.Row(
                        alignment="center",
                        controls=[bubble2, ft.Text("        "), bubble3],
                    ),
                ],
            ),
            ft.Row(
                alignment="center",
                controls=[bubble4, ft.Text("               "), bubble5],
            ),
            ft.Column(
                spacing=-1,
                controls=[
                    ft.Row(
                        alignment="center",
                        controls=[bubble6, ft.Text("        "), bubble7],
                    ),
                    ft.Row(alignment="center", controls=[bubble8]),
                ],
            ),
        ]
    )
    page.add(loading)
    change()


ft.app(target=main)
