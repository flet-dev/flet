import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn InputOTP"

    def handle_change(e: ft.Event[shad.InputOTP]):
        status.value = f"Entered: {e.control.value}"

    def handle_complete(e: ft.Event[shad.InputOTP]):
        status.value = f"Verifying {e.control.value}..."

    def handle_clear(e: ft.Event[shad.Button]):
        otp.value = ""
        status.value = "Enter the code we sent you."

    otp = shad.InputOTP(
        length=6,
        groups=[3, 3],
        on_change=handle_change,
        on_complete=handle_complete,
    )
    status = ft.Text("Enter the code we sent you.")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    otp,
                    status,
                    shad.Button(
                        "Clear",
                        variant=shad.ButtonVariant.OUTLINE,
                        on_click=handle_clear,
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
