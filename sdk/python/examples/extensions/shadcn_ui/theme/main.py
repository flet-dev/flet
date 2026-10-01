import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Theme"

    def handle_scheme_change(e: ft.Event[ft.Dropdown]):
        theme.color_scheme = shad.ColorScheme(e.control.value)

    theme = shad.Theme(
        color_scheme=shad.ColorScheme.VIOLET,
        content=ft.Column(
            controls=[
                ft.Row(
                    wrap=True,
                    controls=[
                        shad.Button("Primary"),
                        shad.Button("Secondary", variant=shad.ButtonVariant.SECONDARY),
                        shad.Button("Outline", variant=shad.ButtonVariant.OUTLINE),
                    ],
                ),
                shad.Checkbox(label="Remember me", value=True),
                shad.Switch(label="Notifications", value=True),
            ],
        ),
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Dropdown(
                        key="color_scheme",
                        label="Color scheme",
                        value=shad.ColorScheme.VIOLET.value,
                        options=[
                            ft.DropdownOption(key=s.value, text=s.name.title())
                            for s in shad.ColorScheme
                        ],
                        on_select=handle_scheme_change,
                    ),
                    theme,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
