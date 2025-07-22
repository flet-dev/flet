import flet as ft

name = "NavigationDrawer example"


def example():
    end_drawer = ft.NavigationDrawer(
        position=ft.NavigationDrawerPosition.END,
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"
            ),
            ft.NavigationDrawerDestination(icon=ft.Icons.ADD_COMMENT, label="Item 2"),
        ],
    )

    drawer = ft.NavigationDrawer(
        controls=[
            ft.NavigationDrawerDestination(
                icon=ft.Icons.ADD_TO_HOME_SCREEN_SHARP, label="Item 1"
            ),
            ft.NavigationDrawerDestination(icon=ft.Icons.ADD_COMMENT, label="Item 2"),
        ],
    )

    def open_end_drawer(e):
        e.control.page.show_dialog(end_drawer)

    def open_drawer(e):
        e.control.page.show_dialog(drawer)

    return ft.Column(
        [
            ft.ElevatedButton("Open end drawer", on_click=open_end_drawer),
            ft.ElevatedButton("Open drawer", on_click=open_drawer),
        ]
    )
