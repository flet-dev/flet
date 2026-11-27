import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent ToggleButton"

    def handle_change(e: ft.Event[fluent.ToggleButton]):
        preview.weight = ft.FontWeight.BOLD if e.control.checked else None
        status.value = "Bold on" if e.control.checked else "Bold off"

    preview = ft.Text("The quick brown fox", size=18)
    status = ft.Text("Bold off")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.ToggleButton("Bold", on_change=handle_change),
                    preview,
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
