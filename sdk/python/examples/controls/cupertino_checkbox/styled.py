import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.Column(
            controls=[
                ft.CupertinoCheckbox(
                    label="Cupertino Checkbox tristate",
                    value=True,
                    tristate=True,
                    check_color=ft.Colors.GREY_900,
                    fill_color={
                        ft.ControlState.HOVERED: ft.Colors.PINK_200,
                        ft.ControlState.PRESSED: ft.Colors.LIME_ACCENT_200,
                        ft.ControlState.SELECTED: ft.Colors.DEEP_ORANGE_200,
                        ft.ControlState.DEFAULT: ft.Colors.TEAL_200,
                    },
                ),
                ft.CupertinoCheckbox(
                    label="Cupertino Checkbox circle border",
                    value=True,
                    shape=ft.CircleBorder(),
                    # scale=ft.Scale(2, alignment=ft.Alignment(-1, 0)),
                ),
                ft.CupertinoCheckbox(
                    label="Cupertino Checkbox border states",
                    value=True,
                    # v1 bug - border_side renders grey box
                    # border_side={
                    #     ft.ControlState.HOVERED: ft.BorderSide(width=5),
                    #     ft.ControlState.DEFAULT: ft.BorderSide(width=3),
                    #     ft.ControlState.FOCUSED: ft.BorderSide(),
                    # },
                    # scale=ft.Scale(2, alignment=ft.Alignment(-0.9, 0)),
                ),
                ft.CupertinoCheckbox(
                    label="Cupertino Checkbox label position",
                    value=True,
                    label_position=ft.LabelPosition.LEFT,
                ),
            ]
        )
    )


ft.run(main)
