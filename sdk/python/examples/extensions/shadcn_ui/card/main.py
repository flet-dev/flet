import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "shadcn/ui Card"

    def handle_create(e: ft.Event[shad.Button]):
        status.value = f"Created project '{name.value}'"

    name = shad.Input(placeholder="Name of your project")
    status = ft.Text()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    shad.Card(
                        width=350,
                        title="Create project",
                        description="Deploy your new project in one-click.",
                        content=ft.Container(
                            padding=ft.Padding.symmetric(vertical=16),
                            content=ft.Column(
                                spacing=6,
                                controls=[ft.Text("Name"), name],
                            ),
                        ),
                        footer=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                shad.Button(
                                    "Cancel", variant=shad.ButtonVariant.OUTLINE
                                ),
                                shad.Button("Deploy", on_click=handle_create),
                            ],
                        ),
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
