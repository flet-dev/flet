import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.Stack(
                width=40,
                height=40,
                controls=[
                    ft.CircleAvatar(
                        foreground_image_src="https://raw.githubusercontent.com/flet-dev/media/98b6df65ba919f2afef284ba04feb2d78f28e1d1/pictures/avatar-user.png"
                    ),
                    ft.Container(
                        alignment=ft.Alignment.BOTTOM_LEFT,
                        content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
