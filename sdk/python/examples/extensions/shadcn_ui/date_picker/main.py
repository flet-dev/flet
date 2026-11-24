import datetime

import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn DatePicker"

    def handle_change(e: ft.Event[shad.DatePicker]):
        value = e.control.value
        selection.value = f"Due date: {value.date() if value else 'none'}"

    selection = ft.Text("Due date: 2025-06-12")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    shad.DatePicker(
                        key="due_date",
                        value=datetime.date(2025, 6, 12),
                        min_date=datetime.date(2025, 6, 1),
                        max_date=datetime.date(2025, 6, 30),
                        on_change=handle_change,
                    ),
                    selection,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
