import flet as ft


def main(page: ft.Page):
    page.title = "Margin Example"

    page.add(
        ft.Row(
            spacing=0,
            controls=[
                ft.Container(
                    content=ft.ElevatedButton("container_1"),
                    bgcolor=ft.Colors.AMBER,
                    # padding=ft.Padding.all(10),
                    margin=ft.Margin.all(10),
                    width=200,
                    height=200,
                ),
                ft.Container(
                    content=ft.ElevatedButton("container_2"),
                    bgcolor=ft.Colors.AMBER,
                    # padding=ft.Padding.all(20),
                    margin=ft.Margin.all(20),
                    width=200,
                    height=200,
                ),
                ft.Container(
                    content=ft.ElevatedButton("container_3"),
                    bgcolor=ft.Colors.AMBER,
                    # padding=ft.Padding.symmetric(horizontal=10),
                    margin=ft.Margin.symmetric(vertical=10),
                    width=200,
                    height=200,
                ),
                ft.Container(
                    content=ft.ElevatedButton("container_4"),
                    bgcolor=ft.Colors.AMBER,
                    # padding=ft.Padding.only(left=10),
                    margin=ft.Margin.only(left=10),
                    width=200,
                    height=200,
                ),
            ],
        )
    )


ft.run(main)
