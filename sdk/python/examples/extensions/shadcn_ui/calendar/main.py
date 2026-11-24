import datetime

import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Calendar"

    def handle_change(e: ft.Event[shad.Calendar]):
        value = e.control.value
        selection.value = f"Selected: {value.date() if value else 'none'}"

    selection = ft.Text("Selected: 2025-06-12")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    shad.Calendar(
                        value=datetime.date(2025, 6, 12),
                        on_change=handle_change,
                    ),
                    selection,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
