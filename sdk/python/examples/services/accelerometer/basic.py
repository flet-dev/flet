import flet as ft


def main(page: ft.Page):
    def handle_reading(e: ft.AccelerometerReadingEvent):
        reading.value = f"x={e.x:.2f} m/s^2, y={e.y:.2f} m/s^2, z={e.z:.2f} m/s^2"
        page.update()

    def handle_error(e: ft.SensorErrorEvent):
        page.add(ft.Text(f"Accelerometer error: {e.message}"))

    page.services.append(
        ft.Accelerometer(
            on_reading=handle_reading,
            on_error=handle_error,
            interval=ft.Duration(milliseconds=100),
            cancel_on_error=False,
        )
    )

    page.add(
        ft.Text("Move your device to see accelerometer readings."),
        reading := ft.Text("Waiting for data..."),
    )


ft.run(main)
