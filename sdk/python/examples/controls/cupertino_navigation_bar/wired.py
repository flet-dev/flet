import flet as ft


def main(page: ft.Page):
    page.title = "CupertinoNavigationBar Example"

    def handle_nav_destination_change(e: ft.Event[ft.CupertinoNavigationBar]):
        if e.control.selected_index == 0:
            body.content.value = "Explore!"
        elif e.control.selected_index == 1:
            body.content.value = "Find Your Way!"
        else:
            body.content.value = "Your Favorites!"
        page.update()

    page.navigation_bar = ft.CupertinoNavigationBar(
        bgcolor=ft.Colors.AMBER_100,
        inactive_color=ft.Colors.GREY,
        active_color=ft.Colors.BLACK,
        on_change=handle_nav_destination_change,
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

    page.add(
        body := ft.SafeArea(content=ft.Text("Explore!")),
    )


if __name__ == "__main__":
    ft.run(main)
