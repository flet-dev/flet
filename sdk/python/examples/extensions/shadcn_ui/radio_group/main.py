import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn RadioGroup"

    def handle_change(e: ft.Event[shad.RadioGroup]):
        selection.value = f"Spacing: {e.control.value}"

    selection = ft.Text("Spacing: comfortable")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    shad.RadioGroup(
                        value="comfortable",
                        on_change=handle_change,
                        items=[
                            shad.Radio(value="default", label="Default"),
                            shad.Radio(value="comfortable", label="Comfortable"),
                            shad.Radio(
                                value="compact",
                                label="Compact",
                                sublabel="Fits more rows on screen.",
                            ),
                        ],
                    ),
                    selection,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
