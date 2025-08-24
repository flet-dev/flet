import flet as ft


def main(page: ft.Page):
    def animate_container(e: ft.Event[ft.Button]):
        container.width = 100 if container.width == 150 else 150
        container.height = 50 if container.height == 150 else 150
        container.bgcolor = (
            ft.Colors.BLUE if container.bgcolor == ft.Colors.RED else ft.Colors.RED
        )
        container.update()

    page.add(
        container := ft.Container(
            width=150,
            height=150,
            bgcolor=ft.Colors.RED,
            animate=ft.Animation(duration=1000, curve=ft.AnimationCurve.BOUNCE_OUT),
        ),
        ft.Button("Animate container", on_click=animate_container),
    )


ft.run(main)
