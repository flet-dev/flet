import flet as ft


def main(page: ft.Page):
    page.add(
        ft.RadioGroup(
            ft.Column(
                controls=[
                    ft.Radio(label="Radio with default style", value="1"),
                    ft.Radio(
                        label="Radio with constant fill color",
                        value="2",
                        fill_color=ft.Colors.RED,
                    ),
                    ft.Radio(
                        label="Radio with dynamic fill color",
                        value="3",
                        fill_color={
                            ft.ControlState.HOVERED: ft.Colors.BLUE,
                            ft.ControlState.SELECTED: ft.Colors.GREEN,
                            ft.ControlState.DEFAULT: ft.Colors.RED,
                        },
                    ),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
