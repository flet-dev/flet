import flet as ft

name = "CupertinoAppBar Example"


def example():
    pagelet = ft.Pagelet(
        appbar=ft.CupertinoAppBar(
            leading=ft.Icon(ft.Icons.PALETTE),
            bgcolor=ft.Colors.YELLOW,
            trailing=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED),
            middle=ft.Text("CupertinoAppBar Middle"),
        ),
        content=ft.Container(),
    )

    return pagelet
