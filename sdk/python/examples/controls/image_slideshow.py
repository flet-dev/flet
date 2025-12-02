import flet as ft


def main(page: ft.Page):
    def animate(e: ft.Event[ft.Button]):
        image1.left = 400 if image1.left == 0 else 0
        image2.left = 0 if image2.left == -400 else -400
        page.update()

    page.add(
        ft.Stack(
            width=200,
            height=300,
            controls=[
                image1 := ft.Image(
                    src="https://picsum.photos/200/300?1",
                    left=0,
                    animate_position=ft.Animation(
                        duration=300,
                        curve=ft.AnimationCurve.BOUNCE_OUT,
                    ),
                ),
                image2 := ft.Image(
                    src="https://picsum.photos/200/300?2",
                    left=-400,
                    animate_position=ft.Animation(
                        duration=300,
                        curve=ft.AnimationCurve.BOUNCE_OUT,
                    ),
                ),
            ],
        ),
        ft.Button("Slide!", on_click=animate),
    )


if __name__ == "__main__":
    ft.run(main)
