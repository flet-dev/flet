import flet as ft

name = "CupertinoTextField example"


def example():
    tf1 = ft.TextField(
        label="Material",
    )
    tf2 = ft.CupertinoTextField(
        placeholder_text="Cupertino",
    )
    tf3 = ft.TextField(
        adaptive=True,
        label="Adaptive",
        tooltip=ft.Tooltip(
            message="Adaptive TextField shows as CupertinoTextField on macOS and iOS and as TextField on other platforms"
        ),
    )

    return ft.Column(controls=[tf1, tf2, tf3])
