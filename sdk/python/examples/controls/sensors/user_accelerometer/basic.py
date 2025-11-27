import flet as ft


def main(page: ft.Page):
    intro = ft.Text(
        "Linear acceleration without gravity. "
        "Keep the app running on a device with motion sensors."
    )
    reading = ft.Text("Waiting for data...")

    def handle_reading(e: ft.UserAccelerometerReadingEvent):
        reading.value = f"x={e.x:.2f} m/s^2, y={e.y:.2f} m/s^2, z={e.z:.2f} m/s^2"
        page.update()

    def handle_error(e: ft.SensorErrorEvent):
        page.add(ft.Text(f"UserAccelerometer error: {e.message}"))

    page.session.store.set(
        "user_accelerometer_service",
        ft.UserAccelerometer(
            on_reading=handle_reading,
            on_error=handle_error,
            interval=ft.Duration(milliseconds=100),
        ),
    )

    page.add(intro, reading)


ft.run(main)
