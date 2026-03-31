import flet as ft


def main(page: ft.Page):
    def handle_reading(e: ft.GyroscopeReadingEvent):
        reading.value = f"x={e.x:.2f} rad/s, y={e.y:.2f} rad/s, z={e.z:.2f} rad/s"

    def handle_error(e: ft.SensorErrorEvent):
        page.add(ft.Text(f"Gyroscope error: {e.message}"))

    page.services.append(
        ft.Gyroscope(
            on_reading=handle_reading,
            on_error=handle_error,
            interval=ft.Duration(milliseconds=100),
        )
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text("Rotate your device to see gyroscope readings."),
                    reading := ft.Text("Waiting for data..."),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
