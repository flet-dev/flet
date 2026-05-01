import flet as ft


def main(page: ft.Page):
    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Checkbox(label="Checkbox with default style"),
                    ft.Checkbox(
                        label="Checkbox with constant fill color",
                        fill_color=ft.Colors.RED,
                        check_color=ft.Colors.YELLOW,
                    ),
                    ft.Row(
                        controls=[
                            ft.Checkbox(
                                key="dynamic_fill_checkbox",
                                fill_color={
                                    ft.ControlState.HOVERED: ft.Colors.BLUE,
                                    ft.ControlState.SELECTED: ft.Colors.GREEN,
                                    ft.ControlState.DEFAULT: ft.Colors.RED,
                                },
                            ),
                            ft.Text("Checkbox with dynamic fill color"),
                        ],
                    ),
                ]
            )
        ),
    )


if __name__ == "__main__":
    ft.run(main)
