import flet as ft

name = "NavigationBar Example"


def example():
    pagelet = ft.Pagelet(
        navigation_bar=ft.NavigationBar(
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
