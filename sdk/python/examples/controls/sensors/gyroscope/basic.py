import flet as ft


def main(page: ft.Page):
    intro = ft.Text("Rotate your device to see gyroscope readings.")
    reading = ft.Text("Waiting for data...")

    def handle_reading(e: ft.GyroscopeReadingEvent):
        reading.value = f"x={e.x:.2f} rad/s, y={e.y:.2f} rad/s, z={e.z:.2f} rad/s"
        page.update()

    def handle_error(e: ft.SensorErrorEvent):
        page.add(ft.Text(f"Gyroscope error: {e.message}"))

    page.session.store.set(
        "gyroscope_service",
        ft.Gyroscope(
            on_reading=handle_reading,
            on_error=handle_error,
            interval=ft.Duration(milliseconds=50),
        ),
    )

    page.add(intro, reading)


ft.run(main)
