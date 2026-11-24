import flet_shadcn_ui as shad

import flet as ft

FRUITS = ["Apple", "Banana", "Blueberry", "Grapes", "Pineapple"]


def main(page: ft.Page):
    page.title = "Shadcn Select"

    def handle_change(e: ft.Event[shad.Select]):
        selection.value = f"Selected: {e.control.value}"

    selection = ft.Text("Selected: None")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    shad.Select(
                        placeholder="Select a fruit",
                        min_width=180,
                        on_change=handle_change,
                        options=[
                            shad.SelectOption(value=fruit.lower(), text=fruit)
                            for fruit in FRUITS
                        ],
                    ),
                    selection,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
