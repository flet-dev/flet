import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "shadcn Input"

    def handle_change(e: ft.Event[shad.Input]):
        echo.value = f"Email: {e.control.value}"

    def handle_submit(e: ft.Event[shad.Input]):
        echo.value = f"Submitted: {e.control.value}"

    echo = ft.Text("Email: ")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=320,
                controls=[
                    shad.Input(
                        key="email",
                        placeholder="Email",
                        keyboard_type=ft.KeyboardType.EMAIL,
                        leading=shad.LucideIcons.MAIL,
                        on_change=handle_change,
                        on_submit=handle_submit,
                    ),
                    shad.Input(
                        placeholder="Password",
                        password=True,
                        leading=shad.LucideIcons.LOCK,
                    ),
                    shad.Input(placeholder="Disabled", disabled=True),
                    echo,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
