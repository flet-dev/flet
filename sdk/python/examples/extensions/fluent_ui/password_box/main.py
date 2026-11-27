import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent PasswordBox"

    def handle_change(e: ft.Event[fluent.PasswordBox]):
        length = len(e.control.value)
        strength.value = (
            "Strength: strong" if length >= 12 else f"Strength: weak ({length}/12)"
        )

    strength = ft.Text("Strength: weak (0/12)")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=300,
                controls=[
                    fluent.PasswordBox(
                        key="password",
                        placeholder="New password",
                        reveal_mode=fluent.PasswordRevealMode.PEEK_ALWAYS,
                        on_change=handle_change,
                    ),
                    strength,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
