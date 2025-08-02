import flet as ft


def main(page: ft.Page):
    def handle_show_drawer(e: ft.Event[ft.FloatingActionButton]):
        pagelet.show_drawer(drawer)

    drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP,
                label="Item 1",
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_COMMENT,
                label="Item 2",
            ),
        ],
    )

    page.add(
        pagelet := ft.Pagelet(
            width=400,
            height=400,
            appbar=ft.AppBar(
                title=ft.Text("Pagelet AppBar Title"),
                bgcolor=ft.Colors.AMBER_ACCENT,
            ),
            content=ft.Container(ft.Text("Pagelet Body"), padding=ft.Padding.all(16)),
            bgcolor=ft.Colors.AMBER_100,
            bottom_appbar=ft.BottomAppBar(
                bgcolor=ft.Colors.BLUE,
                shape=ft.CircularRectangleNotchShape(),
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                        ft.Container(expand=True),
                        ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                        ft.IconButton(
                            icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE
                        ),
                    ]
                ),
            ),
            end_drawer=drawer,
            floating_action_button=ft.FloatingActionButton(
                content="Open",
                shape=ft.CircleBorder(),
                on_click=handle_show_drawer,
            ),
            floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,
        )
    )


ft.run(main)
