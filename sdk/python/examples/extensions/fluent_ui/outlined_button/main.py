import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent OutlinedButton"

    def handle_preview(e: ft.Event[fluent.OutlinedButton]):
        status.value = "Showing preview"

    status = ft.Text("Editing")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            fluent.FilledButton("Publish"),
                            fluent.OutlinedButton("Preview", on_click=handle_preview),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
