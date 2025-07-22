import flet as ft


def main(page: ft.Page):
    def handle_gain_accessibility_focus(e: ft.Event[ft.Semantics]):
        print("focus gained")

    def handle_lose_accessibility_focus(e: ft.Event[ft.Semantics]):
        print("focus lost")

    page.add(
        ft.Column(
            controls=[
                ft.Semantics(
                    label="Input your occupation",
                    on_did_gain_accessibility_focus=handle_gain_accessibility_focus,
                    on_did_lose_accessibility_focus=handle_lose_accessibility_focus,
                    content=ft.TextField(
                        label="Occupation",
                        hint_text="Use 20 words or less",
                        value="What is your occupation?",
                    ),
                ),
                ft.Icon(name="settings", color="#c1c1c1"),
            ]
        )
    )


ft.run(main)
