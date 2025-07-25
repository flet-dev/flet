import flet as ft


def main(page: ft.Page):
    def animate(e: ft.Event[ft.ElevatedButton]):
        container.offset = ft.Offset(0, 0)
        container.update()

    page.add(
        container := ft.Container(
            width=150,
            height=150,
            bgcolor=ft.Colors.BLUE,
            border_radius=ft.BorderRadius.all(10),
            offset=ft.Offset(x=-2, y=0),
            animate_offset=ft.Animation(duration=1000),
        ),
        ft.ElevatedButton("Reveal!", on_click=animate),
    )


ft.run(main)
