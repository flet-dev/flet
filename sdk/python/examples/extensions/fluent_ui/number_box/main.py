import flet_fluent_ui as fluent

import flet as ft

PRICE = 4.5


def main(page: ft.Page):
    page.title = "Fluent NumberBox"

    def handle_change(e: ft.Event[fluent.NumberBox]):
        quantity = e.control.value or 0
        total.value = f"Total: ${quantity * PRICE:.2f}"

    total = ft.Text(f"Total: ${PRICE:.2f}")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=220,
                controls=[
                    ft.Text("Coffee beans, $4.50 per bag"),
                    fluent.NumberBox(
                        key="quantity",
                        value=1,
                        min=1,
                        max=20,
                        precision=0,
                        on_change=handle_change,
                    ),
                    total,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
