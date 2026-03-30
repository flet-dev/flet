import flet as ft


def main(page: ft.Page):
    def animate(e: ft.Event[ft.Button]):
        container.offset = ft.Offset(0, 0)
        container.update()

    page.add(
        container := ft.Container(
            width=150,
            height=150,
            bgcolor=ft.Colors.BLUE,
            border_radius=ft.BorderRadius.all(10),
            offset=ft.Offset(x=-1.1, y=0),
            animate_offset=ft.Animation(
                duration=600,
                curve=ft.AnimationCurve.BOUNCE_OUT,
            ),
        ),
        ft.Button("Reveal!", on_click=animate),
    )


ft.run(main)
