import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent ComboBox"

    def handle_change(e: ft.Event[fluent.ComboBox]):
        status.value = f"Color: {e.control.value}"

    status = ft.Text("No color chosen")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.ComboBox(
                        placeholder="Pick a color",
                        on_change=handle_change,
                        items=[
                            fluent.ComboBoxItem(value="red", text="Red"),
                            fluent.ComboBoxItem(value="green", text="Green"),
                            fluent.ComboBoxItem(value="blue", text="Blue"),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
