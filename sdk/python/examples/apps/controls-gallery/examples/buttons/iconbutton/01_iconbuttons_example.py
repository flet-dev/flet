import flet as ft

name = "IconButtons example"


def example():
    return ft.Row(
        [
            ft.IconButton(
                icon=ft.Icons.PAUSE_CIRCLE_FILLED_ROUNDED,
                icon_color="blue400",
                icon_size=20,
                tooltip="Pause record",
            ),
            ft.IconButton(
                icon=ft.Icons.DELETE_FOREVER_ROUNDED,
                icon_color="pink600",
                icon_size=40,
                tooltip="Delete record",
            ),
        ]
    )
