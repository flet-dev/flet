import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent RadioGroup"

    def handle_change(e: ft.Event[fluent.RadioGroup]):
        status.value = f"Size: {e.control.value}"

    status = ft.Text("Size: medium")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.RadioGroup(
                        value="medium",
                        on_change=handle_change,
                        items=[
                            fluent.RadioButton(value="small", label="Small"),
                            fluent.RadioButton(value="medium", label="Medium"),
                            fluent.RadioButton(value="large", label="Large"),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
