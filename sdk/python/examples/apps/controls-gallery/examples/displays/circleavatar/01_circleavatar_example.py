import flet as ft

name = "CircleAvatar Example"


def example():
    # a "normal" avatar with background image
    a1 = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4",
        content=ft.Text("FF"),
    )
    # avatar with failing foreground image and fallback text
    a2 = ft.CircleAvatar(
        foreground_image_src="https://avatars.githubusercontent.com/u/_5041459?s=88&v=4",
        content=ft.Text("FF"),
    )
    # avatar with icon, aka icon with inverse background
    a3 = ft.CircleAvatar(
        content=ft.Icon(ft.Icons.ABC),
    )
    # avatar with icon and custom colors
    a4 = ft.CircleAvatar(
        content=ft.Icon(ft.Icons.WARNING_ROUNDED),
        color=ft.Colors.YELLOW_200,
        bgcolor=ft.Colors.AMBER_700,
    )
    # avatar with online status
    a5 = ft.Stack(
        [
            ft.CircleAvatar(
                foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
            ),
            ft.Container(
                content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                alignment=ft.Alignment.bottom_left(),
            ),
        ],
        width=40,
        height=40,
    )

    return ft.Column([a1, a2, a3, a4, a5])
