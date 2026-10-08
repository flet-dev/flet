import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Alert"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=420,
                controls=[
                    shad.Alert(
                        icon=shad.LucideIcons.TERMINAL,
                        title="Heads up!",
                        description=(
                            "You can add components to your app using the CLI."
                        ),
                    ),
                    shad.Alert(
                        icon=shad.LucideIcons.CIRCLE_ALERT,
                        title="Error",
                        description="Your session has expired. Please log in again.",
                        variant=shad.AlertVariant.DESTRUCTIVE,
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
