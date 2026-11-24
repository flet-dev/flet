import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Tooltip"

    page.add(
        ft.SafeArea(
            content=ft.Row(
                spacing=16,
                controls=[
                    shad.Tooltip(
                        message="Add to library",
                        content=shad.Button(
                            "Hover me", variant=shad.ButtonVariant.OUTLINE
                        ),
                    ),
                    shad.Tooltip(
                        message=ft.Row(
                            tight=True,
                            controls=[
                                ft.Icon(shad.LucideIcons.KEYBOARD, size=14),
                                ft.Text("Ctrl+S"),
                            ],
                        ),
                        wait_duration=ft.Duration(milliseconds=500),
                        content=shad.IconButton(
                            icon=shad.LucideIcons.SAVE,
                            variant=shad.ButtonVariant.OUTLINE,
                        ),
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
