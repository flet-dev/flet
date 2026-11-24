import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Avatar"

    page.add(
        ft.SafeArea(
            content=ft.Row(
                controls=[
                    shad.Avatar(
                        src="https://raw.githubusercontent.com/flet-dev/media/98b6df65ba919f2afef284ba04feb2d78f28e1d1/pictures/avatar-user.png",
                        placeholder="CN",
                    ),
                    shad.Avatar(placeholder="JD"),
                    shad.Avatar(placeholder="AB", size=56),
                    shad.Avatar(
                        placeholder=ft.Icon(shad.LucideIcons.USER, size=20),
                        bgcolor=ft.Colors.PRIMARY_CONTAINER,
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
