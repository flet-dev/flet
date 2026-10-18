import flet_shadcn_ui as shad

import flet as ft

MAX_LENGTH = 120


def main(page: ft.Page):
    page.title = "Shadcn Textarea"

    def handle_change(e: ft.Event[shad.Textarea]):
        counter.value = f"{len(e.control.value)}/{MAX_LENGTH}"

    counter = ft.Text(f"0/{MAX_LENGTH}", color=ft.Colors.ON_SURFACE_VARIANT)

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=360,
                controls=[
                    ft.Text("Your message"),
                    shad.Textarea(
                        key="message",
                        placeholder="Type your message here.",
                        max_length=MAX_LENGTH,
                        on_change=handle_change,
                    ),
                    counter,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
