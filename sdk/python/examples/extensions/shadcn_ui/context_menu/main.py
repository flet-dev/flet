import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn ContextMenu"

    def handle_click(e: ft.Event[shad.MenuItem]):
        status.value = f"Clicked: {e.control.content}"

    def item(label: str, **kwargs) -> shad.MenuItem:
        return shad.MenuItem(label, on_click=handle_click, **kwargs)

    def divider() -> shad.Separator:
        return shad.Separator(margin=ft.Margin.symmetric(vertical=4))

    status = ft.Text("Right-click the area above")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    shad.ContextMenu(
                        content=ft.Container(
                            key="area",
                            width=300,
                            height=150,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(1, ft.Colors.OUTLINE_VARIANT),
                            border_radius=8,
                            content=ft.Text("Right click here"),
                        ),
                        items=[
                            item("Back", inset=True, trailing="Ctrl+["),
                            item(
                                "Forward", inset=True, trailing="Ctrl+]", disabled=True
                            ),
                            item("Reload", inset=True, trailing="Ctrl+R"),
                            shad.MenuItem(
                                "More Tools",
                                inset=True,
                                items=[
                                    item("Save Page As...", trailing="Ctrl+S"),
                                    item("Create Shortcut..."),
                                    divider(),
                                    item("Developer Tools"),
                                ],
                            ),
                            divider(),
                            item(
                                "Show Bookmarks",
                                leading=shad.LucideIcons.CHECK,
                                trailing="Ctrl+Shift+B",
                            ),
                            item("Show Full URLs", inset=True),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
