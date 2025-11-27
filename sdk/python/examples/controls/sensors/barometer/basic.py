import flet as ft


def main(page: ft.Page):
    intro = ft.Text("Atmospheric pressure (hPa).")
    reading = ft.Text("Waiting for data...")

    def handle_reading(e: ft.BarometerReadingEvent):
        reading.value = f"{e.pressure:.2f} hPa"
        page.update()

    def handle_error(e: ft.SensorErrorEvent):
        page.add(ft.Text(f"Barometer error: {e.message}"))

    page.session.store.set(
        "barometer_service",
        ft.Barometer(
            on_reading=handle_reading,
            on_error=handle_error,
            interval=ft.Duration(milliseconds=500),
        ),
    )

    page.add(intro, reading)


ft.run(main)
