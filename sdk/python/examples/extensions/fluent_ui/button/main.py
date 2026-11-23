import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Button"

    def handle_click(e: ft.Event[ft.Control]):
        status.value = f"Clicked: {e.control.data}"

    status = ft.Text("Click a button")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            fluent.FilledButton(
                                "Save", data="Save", on_click=handle_click
                            ),
                            fluent.Button(
                                "Cancel", data="Cancel", on_click=handle_click
                            ),
                            fluent.OutlinedButton(
                                "Details", data="Details", on_click=handle_click
                            ),
                            fluent.HyperlinkButton(
                                "Learn more", data="Learn more", on_click=handle_click
                            ),
                            fluent.IconButton(
                                fluent.FluentIcons.SETTINGS,
                                data="Settings",
                                tooltip="Settings",
                                on_click=handle_click,
                            ),
                        ],
                    ),
                    fluent.Button("Disabled", disabled=True),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
