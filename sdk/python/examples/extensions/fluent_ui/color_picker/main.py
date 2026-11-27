import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent ColorPicker"

    def handle_change(e: ft.Event[fluent.ColorPicker]):
        swatch.bgcolor = e.control.value
        label.value = e.control.value

    swatch = ft.Container(width=80, height=80, border_radius=8, bgcolor="#ff0078d4")
    label = ft.Text("#ff0078d4")

    page.add(
        ft.SafeArea(
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    fluent.ColorPicker(
                        key="picker",
                        value="#ff0078d4",
                        show_more_button=False,
                        on_change=handle_change,
                    ),
                    ft.Column(controls=[swatch, label]),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
