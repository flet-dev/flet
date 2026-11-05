import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Sonner"

    count = 0

    def add_event(e: ft.Event[shad.Button]):
        nonlocal count
        count += 1
        page.show_dialog(
            shad.Sonner(
                title=f"Event {count} has been created",
                description="Sunday, December 03, 2023 at 9:00 AM",
                action=shad.Button("Undo", on_click=lambda e: page.pop_dialog()),
            )
        )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Text("Each click adds a notification to the stack."),
                    shad.Button(
                        "Add to calendar",
                        variant=shad.ButtonVariant.OUTLINE,
                        on_click=add_event,
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
