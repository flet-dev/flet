import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Slider"

    def handle_change(e: ft.Event[fluent.Slider]):
        status.value = f"Volume: {round(e.control.value)}"

    status = ft.Text("Volume: 40")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=300,
                controls=[
                    fluent.Slider(
                        key="volume",
                        value=40,
                        label="Volume",
                        on_change=handle_change,
                    ),
                    fluent.Slider(value=3, max=5, divisions=5),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
