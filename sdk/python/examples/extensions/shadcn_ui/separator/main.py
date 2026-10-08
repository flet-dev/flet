import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Separator"

    page.add(
        ft.SafeArea(
            content=ft.Column(
                width=320,
                spacing=0,
                controls=[
                    ft.Text("Radix Primitives", weight=ft.FontWeight.W_500),
                    ft.Text(
                        "An open-source UI component library.",
                        color=ft.Colors.ON_SURFACE_VARIANT,
                    ),
                    shad.Separator(),
                    ft.Row(
                        height=20,
                        controls=[
                            ft.Text("Blog"),
                            shad.Separator(vertical=True),
                            ft.Text("Docs"),
                            shad.Separator(vertical=True),
                            ft.Text("Source"),
                        ],
                    ),
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
