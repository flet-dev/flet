import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn IconButton"

    def handle_click(e: ft.Event[shad.IconButton]):
        message.value = f"Clicked: {e.control.data}"

    message = ft.Text("Click a button")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            shad.IconButton(
                                icon=shad.LucideIcons.ROCKET,
                                data="Primary",
                                on_click=handle_click,
                            ),
                            shad.IconButton(
                                icon=shad.LucideIcons.TRASH_2,
                                variant=shad.ButtonVariant.DESTRUCTIVE,
                                data="Destructive",
                                on_click=handle_click,
                            ),
                            shad.IconButton(
                                icon=shad.LucideIcons.SETTINGS,
                                variant=shad.ButtonVariant.OUTLINE,
                                data="Outline",
                                on_click=handle_click,
                            ),
                            shad.IconButton(
                                icon=shad.LucideIcons.COPY,
                                variant=shad.ButtonVariant.SECONDARY,
                                data="Secondary",
                                on_click=handle_click,
                            ),
                            shad.IconButton(
                                icon=shad.LucideIcons.HEART,
                                variant=shad.ButtonVariant.GHOST,
                                data="Ghost",
                                on_click=handle_click,
                            ),
                        ],
                    ),
                    message,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
