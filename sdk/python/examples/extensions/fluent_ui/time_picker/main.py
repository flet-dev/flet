from datetime import time

import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent TimePicker"

    def handle_change(e: ft.Event[fluent.TimePicker]):
        status.value = f"Meeting at {e.control.value:%H:%M}"

    status = ft.Text("Meeting at 14:30")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.TimePicker(header="Alarm", value=time(7, 30)),
                    fluent.TimePicker(
                        key="meeting",
                        header="Meeting (every 5 minutes)",
                        value=time(14, 30),
                        use_24_hour=True,
                        minute_increment=5,
                        on_change=handle_change,
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
