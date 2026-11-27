from datetime import date

import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent CalendarDatePicker"

    def handle_change(e: ft.Event[fluent.CalendarDatePicker]):
        # A picked date arrives in UTC: convert it to the local date.
        day = e.control.value.astimezone()
        status.value = f"Delivery on {day:%A, %B} {day.day}"

    status = ft.Text("Delivery on Wednesday, May 14")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.CalendarDatePicker(
                        key="delivery",
                        value=date(2025, 5, 14),
                        first_date=date(2025, 5, 5),
                        # No deliveries on public holidays.
                        blackout_dates=[date(2025, 5, 26)],
                        on_change=handle_change,
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
