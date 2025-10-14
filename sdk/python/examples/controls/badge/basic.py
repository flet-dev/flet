import flet as ft


def main(page: ft.Page):
    page.title = "Badge example"
    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icon(
                    ft.Icons.EXPLORE,
                    badge=ft.Badge(small_size=10),
                ),
                label="Explore",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.COMMUTE,
                label="Commute",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icon(
                    ft.Icons.PHONE,
                    badge="10",
                )
            ),
        ]
    )
    page.add(ft.Text("Body!"))


if __name__ == "__main__":
    ft.run(main)
