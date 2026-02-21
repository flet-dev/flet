import flet as ft


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def animate(e: ft.Event[ft.Button]):
        image.scale = 30
        image.opacity = 0
        image.update()

    page.add(
        ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                image := ft.Image(
                    src="icon-192.png",
                    width=100,
                    height=100,
                    scale=1.0,
                    animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_IN_QUINT),
                    opacity=1.0,
                    animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_IN_QUINT),
                ),
                ft.Button("Boom!", on_click=animate),
            ],
        )
    )


ft.run(main)
