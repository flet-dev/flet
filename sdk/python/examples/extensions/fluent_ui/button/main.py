import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Button"

    def handle_click(e: ft.Event[fluent.Button]):
        status.value = "Changes discarded"

    status = ft.Text("You have unsaved changes")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            fluent.Button("Discard changes", on_click=handle_click),
                            fluent.Button("Disabled", disabled=True),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
