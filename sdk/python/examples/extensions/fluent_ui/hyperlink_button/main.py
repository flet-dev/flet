import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent HyperlinkButton"

    def handle_forgot(e: ft.Event[fluent.HyperlinkButton]):
        status.value = "Password reset link sent"

    status = ft.Text()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=300,
                controls=[
                    fluent.TextBox(placeholder="Email"),
                    fluent.TextBox(placeholder="Password", password=True),
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            fluent.HyperlinkButton(
                                "Forgot password?", on_click=handle_forgot
                            ),
                            fluent.FilledButton("Sign in"),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
