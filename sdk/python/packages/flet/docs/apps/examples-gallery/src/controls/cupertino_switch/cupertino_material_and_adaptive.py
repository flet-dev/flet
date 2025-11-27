import flet as ft


def main(page: ft.Page):
    page.add(
        ft.CupertinoSwitch(
            label="Cupertino Switch",
            value=True,
        ),
        ft.Switch(
            label="Material Switch",
            value=True,
            thumb_color={ft.ControlState.SELECTED: ft.Colors.BLUE},
            track_color=ft.Colors.YELLOW,
            focus_color=ft.Colors.PURPLE,
        ),
        ft.Container(height=20),
        ft.Text(
            value="Adaptive Switch shows as CupertinoSwitch on macOS and iOS and as Switch on other platforms:"
        ),
        ft.Switch(
            adaptive=True,
            label="Adaptive Switch",
            value=True,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
