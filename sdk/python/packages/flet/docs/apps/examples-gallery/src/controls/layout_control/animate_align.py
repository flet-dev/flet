import flet as ft


def main(page: ft.Page):
    def animate_click():
        txt.align = ft.Alignment.TOP_LEFT

    page.add(
        ft.Stack(
            width=200,
            height=200,
            controls=[
                (
                    txt := ft.Text(
                        "Hello, Flet!",
                        align=ft.Alignment.BOTTOM_RIGHT,
                        animate_align=1000,
                    )
                )
            ],
        ),
        ft.Button("Animate align", on_click=animate_click),
    )


if __name__ == "__main__":
    ft.run(main)
