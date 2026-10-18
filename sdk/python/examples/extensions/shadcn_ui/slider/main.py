import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Slider"

    def handle_change(e: ft.Event[shad.Slider]):
        volume.value = f"Volume: {int(e.control.value)}"

    volume = ft.Text("Volume: 50")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=320,
                spacing=16,
                controls=[
                    volume,
                    shad.Slider(
                        key="volume",
                        value=50,
                        min=0,
                        max=100,
                        divisions=10,
                        on_change=handle_change,
                    ),
                    shad.Slider(value=0.3, disabled=True),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
