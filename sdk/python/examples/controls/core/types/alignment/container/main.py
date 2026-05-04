import flet as ft


def main(page: ft.Page):
    page.title = "Containers with different alignments"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                bgcolor=ft.Colors.AMBER,
                                padding=15,
                                alignment=ft.Alignment.CENTER,
                                width=150,
                                height=150,
                                content=ft.Button("Center"),
                            ),
                            ft.Container(
                                bgcolor=ft.Colors.AMBER,
                                padding=15,
                                alignment=ft.Alignment.TOP_LEFT,
                                width=150,
                                height=150,
                                content=ft.Button("Top left"),
                            ),
                            ft.Container(
                                bgcolor=ft.Colors.AMBER,
                                padding=15,
                                alignment=ft.Alignment(-0.5, -0.5),
                                width=150,
                                height=150,
                                content=ft.Button("-0.5, -0.5"),
                            ),
                        ],
                        wrap=True,
                    )
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
