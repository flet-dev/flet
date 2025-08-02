import flet as ft


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        shape=ft.CircleBorder(),
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.appbar = ft.AppBar(
        title=ft.Text("Bottom AppBar Demo"),
        center_title=True,
        bgcolor=ft.Colors.GREEN_300,
        automatically_imply_leading=False,
    )
    page.bottom_appbar = ft.BottomAppBar(
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
    )

    page.add(ft.Text("Body!"))


ft.run(main)
