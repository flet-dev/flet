import datetime

import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn DateRangePicker"

    def describe(start, end) -> str:
        if start is None:
            return "Trip: not set"
        return f"Trip: {start.date()} to {end.date() if end else '...'}"

    def handle_change(e: ft.Event[shad.DateRangePicker]):
        trip.value = describe(e.control.start_value, e.control.end_value)

    trip = ft.Text("Trip: 2025-06-09 to 2025-06-13")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    shad.DateRangePicker(
                        key="trip",
                        start_value=datetime.date(2025, 6, 9),
                        end_value=datetime.date(2025, 6, 13),
                        on_change=handle_change,
                    ),
                    trip,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
