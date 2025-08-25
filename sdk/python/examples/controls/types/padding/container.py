import flet as ft


def main(page: ft.Page):
    page.title = "Containers with different padding"

    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=ft.Button("container_1"),
                    bgcolor=ft.Colors.AMBER,
                    padding=ft.Padding.all(10),
                    width=150,
                    height=150,
                ),
                ft.Container(
                    content=ft.Button("container_2"),
                    bgcolor=ft.Colors.AMBER,
                    padding=ft.Padding.all(20),
                    width=150,
                    height=150,
                ),
                ft.Container(
                    content=ft.Button("container_3"),
                    bgcolor=ft.Colors.AMBER,
                    padding=ft.Padding.symmetric(horizontal=10),
                    width=150,
                    height=150,
                ),
                ft.Container(
                    content=ft.Button("container_4"),
                    bgcolor=ft.Colors.AMBER,
                    padding=ft.Padding.only(left=10),
                    width=150,
                    height=150,
                ),
            ]
        )
    )


ft.run(main)
