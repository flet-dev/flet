import flet as ft


def main(page: ft.Page):
    def handle_reading(e: ft.BarometerReadingEvent):
        reading.value = f"{e.pressure:.2f} hPa"
        page.update()

    def handle_error(e: ft.SensorErrorEvent):
        page.add(ft.Text(f"Barometer error: {e.message}"))

    page.services.append(
        ft.Barometer(
            on_reading=handle_reading,
            on_error=handle_error,
            interval=ft.Duration(milliseconds=500),
        )
    )

    page.add(
        ft.Text("Atmospheric pressure (hPa)."),
        reading := ft.Text("Waiting for data..."),
    )


ft.run(main)
