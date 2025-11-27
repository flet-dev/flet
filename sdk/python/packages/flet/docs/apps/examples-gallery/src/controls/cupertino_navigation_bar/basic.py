import flet as ft


def main(page: ft.Page):
    page.title = "CupertinoNavigationBar Example"

    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.Colors.AMBER_100,
        inactive_color=ft.Colors.GREY,
        active_color=ft.Colors.BLACK,
        on_change=lambda e: print("Selected tab:", e.control.selected_index),
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.EXPLORE_OUTLINED,
                selected_icon=ft.Icons.EXPLORE,
                label="Explore",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COMMUTE_OUTLINED,
                selected_icon=ft.Icons.COMMUTE,
                label="Commute",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.BOOKMARK_BORDER,
                selected_icon=ft.Icons.BOOKMARK,
                label="Favorites",
            ),
        ],
    )

    page.add(ft.SafeArea(content=ft.Text("Body!")))


if __name__ == "__main__":
    ft.run(main)
