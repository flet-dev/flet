import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent ProgressBar and ProgressRing"

    def advance(e: ft.Event[fluent.Button]):
        value = (bar.value + 25) % 125
        bar.value = value
        ring.value = value
        status.value = f"{value}% done"

    bar = fluent.ProgressBar(value=25, width=300)
    ring = fluent.ProgressRing(value=25)
    status = ft.Text("25% done")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    bar,
                    ring,
                    status,
                    fluent.Button("Advance", on_click=advance),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
