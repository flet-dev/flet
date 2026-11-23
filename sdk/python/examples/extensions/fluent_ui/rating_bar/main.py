import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent RatingBar"

    def handle_change(e: ft.Event[fluent.RatingBar]):
        status.value = f"You rated it {e.control.value:g} stars"

    status = ft.Text("Rate this app")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text("Average"),
                            fluent.RatingBar(value=4.3, read_only=True, icon_size=16),
                            ft.Text("4.3"),
                        ],
                    ),
                    fluent.RatingBar(key="rating", on_change=handle_change),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
