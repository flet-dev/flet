import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Progress"

    def handle_step(e: ft.Event[shad.Button]):
        progress.value = min(1.0, round(progress.value + 0.2, 1))
        label.value = f"{int(progress.value * 100)}%"

    progress = shad.Progress(value=0.2, width=300)
    label = ft.Text("20%")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Row([progress, label]),
                    shad.Button("Step", on_click=handle_step),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
