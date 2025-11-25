import flet as ft

name = "CupertinoSwitch example"


def example():
    c1 = ft.CupertinoSwitch(
        label="Cupertino Switch",
        value=True,
    )
    c2 = ft.Switch(
        label="Material Switch",
        value=True,
    )

    c3 = ft.Switch(
        adaptive=True,
        label="Adaptive Switch",
        value=True,
        tooltip=ft.Tooltip(
            message="Adaptive Switch shows as CupertinoSwitch on macOS and iOS and as Switch on other platforms"
        ),
    )

    return ft.Column(controls=[c1, c2, c3])
