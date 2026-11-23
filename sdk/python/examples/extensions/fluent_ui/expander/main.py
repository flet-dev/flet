import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Expander"

    def handle_change(e: ft.Event[fluent.Expander]):
        status.value = "Expanded" if e.control.expanded else "Collapsed"

    status = ft.Text("Collapsed")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=400,
                controls=[
                    fluent.Expander(
                        header="Advanced options",
                        leading=fluent.FluentIcons.SETTINGS,
                        on_change=handle_change,
                        content=ft.Column(
                            controls=[
                                fluent.Checkbox(label="Enable logging"),
                                fluent.Checkbox(label="Send diagnostics"),
                            ],
                        ),
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
