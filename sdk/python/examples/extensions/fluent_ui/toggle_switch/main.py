import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent ToggleSwitch"

    def handle_change(e: ft.Event[fluent.ToggleSwitch]):
        status.value = "Wi-Fi is on" if e.control.value else "Wi-Fi is off"

    status = ft.Text("Wi-Fi is off")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.ToggleSwitch(label="Wi-Fi", on_change=handle_change),
                    fluent.ToggleSwitch(
                        label="Bluetooth", label_first=True, value=True
                    ),
                    fluent.ToggleSwitch(label="Disabled", disabled=True),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
