import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Card"

    page.add(
        ft.SafeArea(
            content=fluent.Card(
                width=360,
                padding=16,
                content=ft.Column(
                    tight=True,
                    controls=[
                        ft.Text("Storage", size=18, weight=ft.FontWeight.W_600),
                        ft.Text("120 GB of 256 GB used"),
                        fluent.ProgressBar(value=47),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[fluent.Button("Manage storage")],
                        ),
                    ],
                ),
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
