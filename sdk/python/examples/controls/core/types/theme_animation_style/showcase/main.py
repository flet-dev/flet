import flet as ft


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    custom_style = ft.AnimationStyle(
        duration=ft.Duration(seconds=2),
        curve=ft.AnimationCurve.EASE_IN_OUT_CUBIC,
    )

    def apply_style(value: str):
        if value == "default":
            page.theme_animation_style = None
        elif value == "custom":
            page.theme_animation_style = custom_style
        else:
            page.theme_animation_style = ft.AnimationStyle.no_animation()
        page.update()

    def handle_style_change(e: ft.Event[ft.SegmentedButton]):
        apply_style(e.control.selected[0])

    def handle_theme_toggle(e: ft.Event[ft.Button]):
        if page.theme_mode == ft.ThemeMode.LIGHT:
            page.theme_mode = ft.ThemeMode.DARK
            toggle_button.icon = ft.Icons.LIGHT_MODE
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            toggle_button.icon = ft.Icons.DARK_MODE
        page.update()

    toggle_button = ft.Button(
        "Switch Theme Mode",
        icon=ft.Icons.DARK_MODE,
        on_click=handle_theme_toggle,
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
                controls=[
                    ft.SegmentedButton(
                        selected=["default"],
                        on_change=handle_style_change,
                        segments=[
                            ft.Segment(value="default", label=ft.Text("Default")),
                            ft.Segment(value="custom", label=ft.Text("Custom")),
                            ft.Segment(value="none", label=ft.Text("None")),
                        ],
                    ),
                    toggle_button,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
