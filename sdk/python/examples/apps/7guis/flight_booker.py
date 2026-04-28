from datetime import date, datetime, time, timedelta

import flet as ft

ONE_WAY_FLIGHT = "one-way flight"
RETURN_FLIGHT = "return flight"


def as_datetime(value: date) -> datetime:
    """Convert a `date` to a `datetime` with no time."""
    return datetime.combine(value, time.min)


def format_date(value: date) -> str:
    """Format a `date` as 'Mon DD, YYYY'."""
    return value.strftime("%b %d, %Y")


def main(page: ft.Page):
    page.title = "7GUIs - Flight Booker"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    today = date.today()
    departure_date = today + timedelta(days=1)
    return_date = departure_date + timedelta(days=2)

    def handle_departure_picker_change(e: ft.Event[ft.DatePicker]):
        nonlocal departure_date
        if e.control.value is not None:
            departure_date = e.control.value.date()
        refresh_ui()

    def handle_return_picker_change(e: ft.Event[ft.DatePicker]):
        nonlocal return_date
        if e.control.value is not None:
            return_date = e.control.value.date()
        refresh_ui()

    def is_return_trip() -> bool:
        return booking_mode.value == RETURN_FLIGHT

    def is_valid() -> bool:
        return not is_return_trip() or return_date >= departure_date

    def show_departure_picker(e: ft.Event[ft.OutlinedButton]):
        page.show_dialog(
            ft.DatePicker(
                value=as_datetime(departure_date),
                first_date=as_datetime(today),
                last_date=as_datetime(today + timedelta(days=365)),
                on_change=handle_departure_picker_change,
            )
        )

    def show_return_picker(e: ft.Event[ft.OutlinedButton]):
        page.show_dialog(
            ft.DatePicker(
                value=as_datetime(return_date),
                first_date=as_datetime(today),
                last_date=as_datetime(today + timedelta(days=365)),
                on_change=handle_return_picker_change,
            )
        )

    def refresh_ui():
        departure_button.content = format_date(departure_date)
        return_button.content = format_date(return_date)
        return_button.disabled = not is_return_trip()
        book_button.disabled = not is_valid()

        if not is_valid():
            page.show_dialog(
                ft.SnackBar("Return date must be on or after the departure date."),
            )

        page.update()

    def get_booking_confirmation_message() -> str:
        if not is_return_trip():
            return f"One-way flight booked for {format_date(departure_date)}."
        return (
            f"Return flight booked: {format_date(departure_date)} to "
            f"{format_date(return_date)}."
        )

    def book(e: ft.Event[ft.Button]):
        page.show_dialog(ft.SnackBar(get_booking_confirmation_message(), action="OK"))

    page.add(
        ft.SafeArea(
            ft.Container(
                width=500,
                padding=28,
                border_radius=24,
                bgcolor=ft.Colors.LIGHT_BLUE_50,
                content=ft.Column(
                    tight=True,
                    spacing=18,
                    controls=[
                        ft.Text("Flight Booker", size=28, weight=ft.FontWeight.W_700),
                        ft.Text(
                            "Switch between one-way and return flights and book.",
                            color=ft.Colors.BLUE_GREY_700,
                        ),
                        booking_mode := ft.Dropdown(
                            width=220,
                            value=ONE_WAY_FLIGHT,
                            on_select=lambda e: refresh_ui(),
                            options=[
                                ft.DropdownOption(
                                    key=ONE_WAY_FLIGHT, text=ONE_WAY_FLIGHT
                                ),
                                ft.DropdownOption(
                                    key=RETURN_FLIGHT, text=RETURN_FLIGHT
                                ),
                            ],
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                departure_button := ft.OutlinedButton(
                                    width=180,
                                    icon=ft.Icons.CALENDAR_MONTH,
                                    on_click=show_departure_picker,
                                ),
                                return_button := ft.OutlinedButton(
                                    width=180,
                                    icon=ft.Icons.EVENT_REPEAT,
                                    on_click=show_return_picker,
                                ),
                            ],
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                book_button := ft.FilledButton(
                                    "Book",
                                    icon=ft.Icons.FLIGHT_TAKEOFF,
                                    on_click=book,
                                )
                            ],
                        ),
                    ],
                ),
            )
        )
    )
    refresh_ui()


if __name__ == "__main__":
    ft.run(main)
