import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent InfoLabel"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=320,
                spacing=16,
                controls=[
                    fluent.InfoLabel(
                        label="Full name",
                        content=fluent.TextBox(placeholder="Jane Doe"),
                    ),
                    fluent.InfoLabel(
                        label="Email",
                        content=fluent.TextBox(placeholder="jane@example.com"),
                    ),
                    fluent.InfoLabel(
                        label="Subscribe to the newsletter",
                        horizontal=True,
                        content=fluent.ToggleSwitch(value=True),
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
