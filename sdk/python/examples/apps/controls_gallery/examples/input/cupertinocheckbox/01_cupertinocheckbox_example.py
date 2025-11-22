import flet as ft

name = "CupertinoCheckbox example"


def example():
    return ft.Column(
        controls=[
            ft.CupertinoCheckbox(label="Cupertino Checkbox", value=True),
            ft.Checkbox(label="Material Checkbox", value=True),
            ft.Checkbox(
                adaptive=True,
                label="Adaptive Checkbox",
                value=True,
                tooltip=ft.Tooltip(
                    message="Adaptive Checkbox shows as CupertinoCheckbox on macOS and iOS and as Checkbox on other platforms"
                ),
            ),
        ]
    )
