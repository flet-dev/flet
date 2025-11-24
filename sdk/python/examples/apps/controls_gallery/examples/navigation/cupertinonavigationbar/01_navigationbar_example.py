import flet as ft

name = "CupertinoNavigationBar Example"


def example():
    pagelet = ft.Pagelet(
        navigation_bar=ft.CupertinoNavigationBar(
            bgcolor=ft.Colors.AMBER_100,
            inactive_color=ft.Colors.GREY,
            active_color=ft.Colors.BLACK,
            on_change=lambda e: print("Selected tab:", e.control.selected_index),
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Explore"),
                ft.NavigationBarDestination(icon=ft.Icons.COMMUTE, label="Commute"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.BOOKMARK_BORDER,
                    selected_icon=ft.Icons.BOOKMARK,
                    label="Explore",
                ),
            ],
        ),
        content=ft.Container(),
        height=400,
    )

    return pagelet
