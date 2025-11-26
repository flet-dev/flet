import flet as ft


def main(page: ft.Page):
    page.add(
        # a "normal" avatar with background image
        ft.CircleAvatar(
            foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
            content=ft.Text("FF"),
        ),
        # avatar with failing foreground image and fallback text
        ft.CircleAvatar(
            foreground_image_src="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
            content=ft.Text("FF"),
        ),
        # avatar with icon, aka icon with inverse background
        ft.CircleAvatar(content=ft.Icon(ft.Icons.ABC)),
        # avatar with icon and custom colors
        ft.CircleAvatar(
            content=ft.Icon(ft.Icons.WARNING_ROUNDED),
            color=ft.Colors.YELLOW_200,
            bgcolor=ft.Colors.AMBER_700,
        ),
        # avatar with online status
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
        ),
    )


if __name__ == "__main__":
    ft.run(main)
