import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "shadcn/ui Checkbox"

    def handle_change(e: ft.Event[shad.Checkbox]):
        status.value = "Accepted" if e.control.value else "Not accepted"

    status = ft.Text("Not accepted")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    shad.Checkbox(
                        label="Accept terms and conditions",
                        sublabel=(
                            "You agree to our Terms of Service and Privacy Policy."
                        ),
                        on_change=handle_change,
                    ),
                    shad.Checkbox(label="Disabled", value=True, disabled=True),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
