import flet as ft


def main(page: ft.Page):
    page.title = "Containers with different alignments"

    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=ft.Button("Center"),
                    bgcolor=ft.Colors.AMBER,
                    padding=15,
                    alignment=ft.Alignment.CENTER,
                    width=150,
                    height=150,
                ),
                ft.Container(
                    content=ft.Button("Top left"),
                    bgcolor=ft.Colors.AMBER,
                    padding=15,
                    alignment=ft.Alignment.TOP_LEFT,
                    width=150,
                    height=150,
                ),
                ft.Container(
                    content=ft.Button("-0.5, -0.5"),
                    bgcolor=ft.Colors.AMBER,
                    padding=15,
                    alignment=ft.Alignment(-0.5, -0.5),
                    width=150,
                    height=150,
                ),
            ]
        )
    )


ft.run(main)
