import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Badge"

    def handle_click(e: ft.Event[shad.Badge]):
        message.value = f"Clicked: {e.control.content}"

    message = ft.Text("Click a badge")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            shad.Badge(v.name.title(), variant=v, on_click=handle_click)
                            for v in shad.BadgeVariant
                        ],
                    ),
                    message,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
