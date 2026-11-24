import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Sheet"

    def handle_dismiss(e: ft.Event[shad.Sheet]):
        # Closing a dialog sends its own update, so the page is not
        # auto-updated after this handler; send the status change explicitly.
        status.value = f"Closed the {e.control.side.value} sheet"
        status.update()

    def open_sheet(side: shad.SheetSide):
        page.show_dialog(
            shad.Sheet(
                side=side,
                title="Edit profile",
                description="Make changes to your profile here.",
                content=ft.Container(
                    padding=ft.Padding.symmetric(vertical=16),
                    content=ft.Column(
                        tight=True,
                        controls=[
                            ft.Text("Name"),
                            shad.Input(value="Pedro Duarte", width=300),
                        ],
                    ),
                ),
                actions=[
                    shad.Button("Save changes", on_click=lambda e: page.pop_dialog())
                ],
                on_dismiss=handle_dismiss,
            )
        )

    status = ft.Text("Open a sheet from any side")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    ft.Row(
                        controls=[
                            shad.Button(
                                side.value.title(),
                                variant=shad.ButtonVariant.OUTLINE,
                                on_click=lambda e, side=side: open_sheet(side),
                            )
                            for side in shad.SheetSide
                        ]
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
