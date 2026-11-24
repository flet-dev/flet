import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Breadcrumb"

    def handle_click(e: ft.Event[shad.BreadcrumbItem]):
        message.value = f"Navigate to: {e.control.content}"

    message = ft.Text("Click a link")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=20,
                controls=[
                    shad.Breadcrumb(
                        items=[
                            shad.BreadcrumbItem("Home", on_click=handle_click),
                            shad.BreadcrumbEllipsis(),
                            shad.BreadcrumbItem("Components", on_click=handle_click),
                            shad.BreadcrumbItem("Breadcrumb"),
                        ]
                    ),
                    shad.Breadcrumb(
                        separator=ft.Text("/"),
                        items=[
                            shad.BreadcrumbItem("Docs", on_click=handle_click),
                            shad.BreadcrumbItem("Controls", on_click=handle_click),
                            shad.BreadcrumbItem("Shadcn"),
                        ],
                    ),
                    message,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
