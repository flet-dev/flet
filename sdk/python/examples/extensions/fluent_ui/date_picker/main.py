from datetime import date

import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent DatePicker"

    def handle_change(e: ft.Event[fluent.DatePicker]):
        # A picked date arrives in UTC: convert it to the local date.
        day = e.control.value.astimezone()
        status.value = f"Birthday: {day:%B} {day.day}, {day.year}"

    status = ft.Text("Birthday: April 12, 1990")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.DatePicker(
                        key="birthday",
                        header="Birthday",
                        value=date(1990, 4, 12),
                        on_change=handle_change,
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
