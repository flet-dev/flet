import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Toast"

    def undo(e: ft.Event[shad.Button]):
        page.pop_dialog()
        # pop_dialog() sends its own update, so the page is not auto-updated
        # after this handler; send the status change explicitly.
        status.value = "Undone"
        status.update()

    def show_toast(e: ft.Event[shad.Button]):
        page.show_dialog(
            shad.Toast(
                title="Scheduled: Catch up",
                description="Friday, February 10, 2023 at 5:57 PM",
                action=shad.Button(
                    "Undo", variant=shad.ButtonVariant.OUTLINE, on_click=undo
                ),
            )
        )

    def show_error(e: ft.Event[shad.Button]):
        page.show_dialog(
            shad.Toast(
                variant=shad.ToastVariant.DESTRUCTIVE,
                title="Uh oh! Something went wrong.",
                description="There was a problem with your request.",
                action=shad.Button(
                    "Try again",
                    variant=shad.ButtonVariant.DESTRUCTIVE,
                    on_click=lambda e: page.pop_dialog(),
                ),
            )
        )

    status = ft.Text("Show a toast")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Row(
                        controls=[
                            shad.Button(
                                "Show toast",
                                variant=shad.ButtonVariant.OUTLINE,
                                on_click=show_toast,
                            ),
                            shad.Button(
                                "Show error",
                                variant=shad.ButtonVariant.OUTLINE,
                                on_click=show_error,
                            ),
                        ]
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
