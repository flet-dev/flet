import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Checkbox(label="Checkbox with default style"),
        ft.Checkbox(
            label="Checkbox with constant fill color",
            fill_color=ft.Colors.RED,
            check_color=ft.Colors.YELLOW,
        ),
        ft.Checkbox(
            label="Checkbox with dynamic fill color",
            fill_color={
                ft.ControlState.HOVERED: ft.Colors.BLUE,
                ft.ControlState.SELECTED: ft.Colors.GREEN,
                ft.ControlState.DEFAULT: ft.Colors.RED,
            },
            # border_side={ft.ControlState.HOVERED: ft.BorderSide(width=1.0)},
        ),
    )


if __name__ == "__main__":
    ft.run(main)
