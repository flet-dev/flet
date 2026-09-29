import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "shadcn/ui Button"

    def handle_click(e: ft.Event[shad.Button]):
        message.value = f"Clicked: {e.control.content}"

    message = ft.Text("Click a button")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=20,
                controls=[
                    ft.Row(
                        wrap=True,
                        controls=[
                            shad.Button(
                                v.name.title(), variant=v, on_click=handle_click
                            )
                            for v in shad.ButtonVariant
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        controls=[
                            shad.Button(s.name.title(), size=s, on_click=handle_click)
                            for s in shad.ButtonSize
                        ],
                    ),
                    ft.Row(
                        wrap=True,
                        controls=[
                            shad.Button(
                                "Login with Email",
                                leading=shad.LucideIcons.MAIL,
                                on_click=handle_click,
                            ),
                            shad.Button(
                                "Next",
                                trailing=shad.LucideIcons.CHEVRON_RIGHT,
                                variant=shad.ButtonVariant.OUTLINE,
                                on_click=handle_click,
                            ),
                            shad.Button("Disabled", disabled=True),
                        ],
                    ),
                    message,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
