import flet as ft

name = "Banner with leading icon and actions"


def example():
    def close_banner(e):
        e.control.page.pop_dialog()

    banner = ft.Banner(
        bgcolor=ft.Colors.AMBER_100,
        leading=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color=ft.Colors.AMBER, size=40),
        content=ft.Text(
            "Oops, there were some errors while trying to delete the file. What would "
            "you like me to do?"
        ),
        actions=[
            ft.TextButton("Retry", on_click=close_banner),
            ft.TextButton("Ignore", on_click=close_banner),
            ft.TextButton("Cancel", on_click=close_banner),
        ],
    )

    def show_banner_click(e):
        e.control.page.show_dialog(banner)

    return ft.Button("Show Banner", on_click=show_banner_click)
