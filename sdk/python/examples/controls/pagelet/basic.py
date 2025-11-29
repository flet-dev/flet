import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.vertical_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        pagelet := ft.Pagelet(
            width=500,
            height=500,
            appbar=ft.AppBar(
                title=ft.Text("Pagelet AppBar"),
                center_title=True,
                bgcolor=ft.Colors.RED_500,
            ),
            content=ft.Text("Pagelet Body"),
            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
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
            drawer=ft.NavigationDrawer(
                on_dismiss=lambda e: print("Drawer dismissed"),
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
                on_dismiss=lambda e: print("End Drawer dismissed"),
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
                icon=ft.Icons.ADD,
                shape=ft.CircleBorder(),
            ),
            floating_action_button_location=ft.FloatingActionButtonLocation.CENTER_DOCKED,
        )
    )


if __name__ == "__main__":
    ft.run(main)
