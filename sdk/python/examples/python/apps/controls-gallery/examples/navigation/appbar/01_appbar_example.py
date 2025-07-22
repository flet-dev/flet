import flet as ft

name = "AppBar Example"


def example():
    pagelet = ft.Pagelet(
        appbar=ft.AppBar(
            leading=ft.Icon(ft.Icons.PALETTE),
            leading_width=40,
            title=ft.Text("AppBar Title"),
            center_title=False,
            bgcolor=ft.Colors.PRIMARY_CONTAINER,
            actions=[
                ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
                ft.IconButton(ft.Icons.FILTER_3),
                ft.PopupMenuButton(
                    items=[
                        ft.PopupMenuItem(text="Item 1"),
                        ft.PopupMenuItem(),  # divider
                        ft.PopupMenuItem(
                            text="Checked item",
                            checked=False,
                        ),
                    ]
                ),
            ],
        ),
        content=ft.Container(),
        height=200,
    )

    return pagelet
