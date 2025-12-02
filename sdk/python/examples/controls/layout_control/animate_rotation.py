from math import pi

import flet as ft


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 30

    def animate(e: ft.Event[ft.Button]):
        container.rotate.angle += pi / 2
        page.update()

    page.add(
        container := ft.Container(
            width=100,
            height=70,
            bgcolor=ft.Colors.BLUE,
            border_radius=5,
            rotate=ft.Rotate(angle=0, alignment=ft.Alignment.CENTER),
            animate_rotation=ft.Animation(
                duration=300, curve=ft.AnimationCurve.BOUNCE_OUT
            ),
        ),
        ft.Button("Animate!", on_click=animate),
    )


if __name__ == "__main__":
    ft.run(main)
