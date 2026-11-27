import flet_fluent_ui as fluent

import flet as ft

COLORS = {
    "Yellow": ft.Colors.YELLOW_200,
    "Green": ft.Colors.GREEN_200,
    "Blue": ft.Colors.BLUE_200,
}


def main(page: ft.Page):
    page.title = "Fluent SplitButton"

    color = "Yellow"

    def highlight(e: ft.Event[fluent.SplitButton]):
        sample.bgcolor = COLORS[color]

    def pick_color(e: ft.Event[fluent.MenuFlyoutItem]):
        nonlocal color
        color = e.control.content
        button.content = f"Highlight: {color}"
        sample.bgcolor = COLORS[color]

    button = fluent.SplitButton(
        "Highlight: Yellow",
        on_click=highlight,
        items=[
            fluent.MenuFlyoutItem(
                name,
                leading=ft.Container(width=12, height=12, bgcolor=value),
                on_click=pick_color,
            )
            for name, value in COLORS.items()
        ],
    )
    sample = ft.Container(
        padding=4,
        content=ft.Text("The meeting moved to Thursday."),
    )

    page.add(ft.SafeArea(content=ft.Column(controls=[button, sample])))


if __name__ == "__main__":
    ft.run(main)
