import flet as ft


def main(page: ft.Page):
    page.title = "Containers with different borders"

    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.AMBER,
                    padding=15,
                    border=ft.Border.all(10, ft.Colors.PINK_600),
                    border_radius=ft.border_radius.all(30),
                    width=150,
                    height=150,
                ),
                ft.Container(
                    bgcolor=ft.Colors.DEEP_PURPLE,
                    padding=15,
                    border=ft.Border.all(3, ft.Colors.LIGHT_GREEN_ACCENT),
                    border_radius=ft.border_radius.only(top_left=10, bottom_right=10),
                    width=150,
                    height=150,
                ),
                ft.Container(
                    bgcolor=ft.Colors.BLUE_GREY_900,
                    padding=15,
                    border=ft.Border.symmetric(
                        vertical=ft.BorderSide(8, ft.Colors.YELLOW_800)
                    ),
                    width=150,
                    height=150,
                ),
            ]
        )
    )


ft.run(main)
