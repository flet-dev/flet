import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Theme"

    def preview(accent_color: ft.ColorValue | None):
        return fluent.Theme(
            accent_color=accent_color,
            content=ft.Column(
                tight=True,
                controls=[
                    fluent.FilledButton("Continue"),
                    fluent.Checkbox(label="Checked", value=True),
                    fluent.ToggleSwitch(label="On", value=True),
                    fluent.ProgressBar(value=60, width=160),
                ],
            ),
        )

    page.add(
        ft.SafeArea(
            content=ft.Row(
                spacing=32,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    preview(None),
                    preview(ft.Colors.PURPLE),
                    preview("#107C10"),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
