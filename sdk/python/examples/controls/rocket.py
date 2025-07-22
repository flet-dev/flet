from math import pi

import flet as ft


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def animate(e: ft.Event[ft.ElevatedButton]):
        container.rotate.angle -= 0.5 * pi
        container.content.scale = 2.0 if container.content.scale == 1.0 else 1.0
        container.content.opacity = 0.4 if container.content.scale == 1.0 else 1.0
        page.update()

    page.add(
        ft.Column(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            height=300,
            controls=[
                container := ft.Container(
                    width=120,
                    height=70,
                    alignment=ft.Alignment.CENTER_RIGHT,
                    rotate=ft.Rotate(0, alignment=ft.Alignment.CENTER_LEFT),
                    animate_rotation=ft.Animation(duration=1000),
                    content=ft.Container(
                        scale=1.0,
                        animate_scale=1000,
                        opacity=1.0,
                        animate_opacity=True,
                        content=ft.Icon(
                            ft.Icons.ROCKET,
                            size=40,
                            color=ft.Colors.BLACK,
                        ),
                    ),
                ),
                ft.ElevatedButton("Launch!", on_click=animate),
            ],
        )
    )


ft.run(main)
