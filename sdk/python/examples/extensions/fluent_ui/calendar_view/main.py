from datetime import date

import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent CalendarView"

    def handle_change(e: fluent.CalendarViewChangeEvent):
        start, end = e.control.value, e.control.end_value
        if start is None:
            status.value = "Pick the first day of your trip"
        elif end is None:
            status.value = "Now pick the last day"
        else:
            # Picked dates arrive in UTC: convert them to local dates.
            days = (end.astimezone() - start.astimezone()).days + 1
            status.value = f"Your trip is {days} days long"

    status = ft.Text("Your trip is 5 days long")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.CalendarView(
                        key="calendar",
                        width=300,
                        selection_mode=fluent.CalendarSelectionMode.RANGE,
                        value=date(2025, 5, 12),
                        end_value=date(2025, 5, 16),
                        # The office is closed on these days.
                        blackout_dates=[date(2025, 5, 1), date(2025, 5, 26)],
                        on_change=handle_change,
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
