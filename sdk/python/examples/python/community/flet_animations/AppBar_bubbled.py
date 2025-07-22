import flet as ft


def main(page: ft.Page):
    def resize_app_bar(i):
        row_.spacing = page.width / 3
        page.update()

    def change_pos(i):
        if i == 1:
            page.floating_action_button_location = (
                ft.FloatingActionButtonLocation.START_DOCKED
            )
            fab.icon = ft.Icons.MENU
            row_.controls = [nothing, second, third]
        elif i == 2:
            page.floating_action_button_location = (
                ft.FloatingActionButtonLocation.CENTER_DOCKED
            )
            fab.icon = ft.Icons.SEARCH
            row_.controls = [first, nothing, third]
        else:
            page.floating_action_button_location = (
                ft.FloatingActionButtonLocation.END_DOCKED
            )
            fab.icon = ft.Icons.FAVORITE
            row_.controls = [first, second, nothing]
        page.update()

    page.horizontal_alignment = page.vertical_alignment = "center"
    fab = ft.FloatingActionButton(
        icon=ft.Icons.SEARCH,
        shape=ft.RoundedRectangleBorder(radius=40),
    )
    page.floating_action_button = fab
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_DOCKED

    page.appbar = ft.AppBar(
        title=ft.Text("Bottom AppBar Demo"),
        center_title=True,
        bgcolor=ft.Colors.GREEN_300,
        automatically_imply_leading=False,
    )
    first = ft.IconButton(
        icon=ft.Icons.MENU,
        icon_size=30,
        tooltip="Menu",
        on_click=lambda i: [change_pos(1)],
    )
    second = ft.IconButton(
        icon=ft.Icons.SEARCH,
        icon_size=30,
        tooltip="Search",
        on_click=lambda i: [change_pos(2)],
    )
    third = ft.IconButton(
        icon=ft.Icons.FAVORITE,
        icon_size=30,
        tooltip="Favourties",
        on_click=lambda i: [change_pos(3)],
    )
    nothing = ft.Text("            ")
    row_ = ft.Row(
        spacing=((page.width / 100) * 129.1) / 3, controls=[first, nothing, third]
    )
    page.bottom_appbar = ft.BottomAppBar(
        bgcolor=ft.Colors.BLUE,
        shape=ft.NotchShape.CIRCULAR,
        notch_margin=5,
        content=row_,
    )
    page.on_resize = resize_app_bar

    page.add(ft.Text("Body!"))


ft.app(target=main)
