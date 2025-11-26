import math

import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Container(
            alignment=ft.Alignment.CENTER,
            width=150,
            height=150,
            border_radius=ft.BorderRadius.all(5),
            gradient=ft.LinearGradient(
                begin=ft.Alignment.TOP_LEFT,
                end=ft.Alignment(0.8, 1),
                tile_mode=ft.GradientTileMode.MIRROR,
                rotation=math.pi / 3,
                colors=[
                    "0xff1f005c",
                    "0xff5b0060",
                    "0xff870160",
                    "0xffac255e",
                    "0xffca485c",
                    "0xffe16b5c",
                    "0xfff39060",
                    "0xffffb56b",
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
