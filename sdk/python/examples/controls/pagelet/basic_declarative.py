import flet as ft


@ft.component
def App():
    async def handle_show_drawer():
        await p.show_drawer()

    async def handle_show_end_drawer():
        await p.show_end_drawer()

    p = ft.Pagelet(
        width=400,
        height=400,
        appbar=ft.AppBar(
            title=ft.Text("Pagelet AppBar Title"),
            bgcolor=ft.Colors.AMBER_ACCENT,
        ),
        content=ft.Container(
            ft.Column(
                [
                    ft.Text("Pagelet Body"),
                    ft.Button("Show end drawer", on_click=handle_show_end_drawer),
                ]
            ),
            padding=ft.Padding.all(16),
        ),
        bgcolor=ft.Colors.AMBER_100,
        bottom_appbar=ft.BottomAppBar(
            bgcolor=ft.Colors.BLUE,
            shape=ft.CircularRectangleNotchShape(),
            content=ft.Row(
                controls=[
                    ft.IconButton(icon=ft.Icons.MENU, icon_color=ft.Colors.WHITE),
                    ft.Container(expand=True),
                    ft.IconButton(icon=ft.Icons.SEARCH, icon_color=ft.Colors.WHITE),
                    ft.IconButton(icon=ft.Icons.FAVORITE, icon_color=ft.Colors.WHITE),
                ]
            ),
        ),
        drawer=ft.NavigationDrawer(
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
        ),
        end_drawer=ft.NavigationDrawer(
            controls=[
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.SLOW_MOTION_VIDEO,
                    label="Item 3",
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icons.INSERT_CHART,
                    label="Item 4",
                ),
            ],
        ),
        floating_action_button=ft.FloatingActionButton(
            content="Open",
            shape=ft.CircleBorder(),
            on_click=handle_show_drawer,
        ),
        floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,
    )
    return p


ft.run(lambda page: page.render(App))
