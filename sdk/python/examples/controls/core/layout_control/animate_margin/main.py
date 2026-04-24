import flet as ft


def main(page: ft.Page):
    def animate_click(e: ft.Event[ft.Button]):
        c.margin = 0
        txt.margin = ft.Margin.only(left=50, top=70)
        c.update()
        txt.update()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    c := ft.Container(
                        width=200,
                        height=200,
                        bgcolor=ft.Colors.AMBER,
                        margin=40,
                        animate=True,
                        content=(
                            txt := ft.Text(
                                "Hello, Flet!",
                                margin=20,
                                animate_margin=1000,
                            )
                        ),
                    ),
                    ft.Button("Animate margin", on_click=animate_click),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
