import flet as ft


def main(page: ft.Page):
    intro = ft.Text("Monitor the ambient magnetic field (uT).")
    reading = ft.Text("Waiting for data...")

    def handle_reading(e: ft.MagnetometerReadingEvent):
        reading.value = f"x={e.x:.2f} uT, y={e.y:.2f} uT, z={e.z:.2f} uT"
        page.update()

    def handle_error(e: ft.SensorErrorEvent):
        page.add(ft.Text(f"Magnetometer error: {e.message}"))

    page.session.store.set(
        "magnetometer_service",
        ft.Magnetometer(
            on_reading=handle_reading,
            on_error=handle_error,
            interval=ft.Duration(milliseconds=200),
        ),
    )

    page.add(intro, reading)


ft.run(main)
