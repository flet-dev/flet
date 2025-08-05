import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Stack(
            width=40,
            height=40,
            controls=[
                ft.CircleAvatar(
                    foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                    alignment=ft.Alignment.BOTTOM_LEFT,
                ),
            ],
        )
    )


ft.run(main)
