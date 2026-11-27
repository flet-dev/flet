import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent Divider"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=320,
                controls=[
                    ft.Text("Account", weight=ft.FontWeight.W_600),
                    ft.Text("Signed in as jane@example.com"),
                    fluent.Divider(),
                    ft.Text("Storage", weight=ft.FontWeight.W_600),
                    ft.Text("120 GB of 256 GB used"),
                    fluent.Divider(),
                    ft.Row(
                        controls=[
                            ft.Text("Help"),
                            fluent.Divider(vertical=True, size=16),
                            ft.Text("Privacy"),
                            fluent.Divider(vertical=True, size=16),
                            ft.Text("Terms"),
                        ],
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
