import flet as ft


def main(page: ft.Page):
    def animate_opacity(e: ft.Event[ft.Button]):
        container.opacity = 0 if container.opacity == 1 else 1
        container.update()

    page.add(
        container := ft.Container(
            width=150,
            height=150,
            bgcolor=ft.Colors.BLUE,
            border_radius=10,
            animate_opacity=300,
        ),
        ft.Button(
            content="Animate opacity",
            on_click=animate_opacity,
        ),
    )


ft.run(main)
