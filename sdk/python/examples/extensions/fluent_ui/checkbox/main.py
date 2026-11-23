import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Checkbox"

    def handle_change(e: ft.Event[fluent.Checkbox]):
        status.value = "Accepted" if e.control.value else "Not accepted"

    status = ft.Text("Not accepted")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.Checkbox(
                        label="Accept terms and conditions",
                        on_change=handle_change,
                    ),
                    fluent.Checkbox(
                        label="Select all (tristate)", tristate=True, value=None
                    ),
                    fluent.Checkbox(label="Disabled", value=True, disabled=True),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
