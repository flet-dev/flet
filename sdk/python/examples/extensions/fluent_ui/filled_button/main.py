import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent FilledButton"

    def handle_save(e: ft.Event[fluent.FilledButton]):
        status.value = "Document saved"

    status = ft.Text("Draft")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            fluent.FilledButton("Save", on_click=handle_save),
                            fluent.Button("Cancel"),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
