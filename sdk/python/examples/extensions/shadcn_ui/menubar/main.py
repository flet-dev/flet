import flet_shadcn_ui as shad

import flet as ft


def main(page: ft.Page):
    page.title = "Shadcn Menubar"

    def handle_click(e: ft.Event[shad.MenuItem]):
        status.value = f"Clicked: {e.control.content}"

    def item(label: str, **kwargs) -> shad.MenuItem:
        return shad.MenuItem(label, on_click=handle_click, **kwargs)

    def divider() -> shad.Separator:
        return shad.Separator(margin=ft.Margin.symmetric(vertical=4))

    status = ft.Text("Pick a menu item")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                spacing=16,
                controls=[
                    shad.Menubar(
                        items=[
                            shad.MenubarItem(
                                "File",
                                items=[
                                    item("New Tab", trailing="Ctrl+T"),
                                    item("New Window", trailing="Ctrl+N"),
                                    item("New Incognito Window", disabled=True),
                                    divider(),
                                    shad.MenuItem(
                                        "Share",
                                        items=[
                                            item("Email link"),
                                            item("Messages"),
                                            item("Notes"),
                                        ],
                                    ),
                                    divider(),
                                    item("Print...", trailing="Ctrl+P"),
                                ],
                            ),
                            shad.MenubarItem(
                                "Edit",
                                items=[
                                    item("Undo", trailing="Ctrl+Z"),
                                    item("Redo", trailing="Ctrl+Shift+Z"),
                                    divider(),
                                    item("Cut"),
                                    item("Copy"),
                                    item("Paste"),
                                ],
                            ),
                            shad.MenubarItem(
                                "View",
                                items=[
                                    item(
                                        "Show Bookmarks Bar",
                                        leading=shad.LucideIcons.CHECK,
                                    ),
                                    item("Show Full URLs", inset=True),
                                    divider(),
                                    item("Reload", inset=True, trailing="Ctrl+R"),
                                ],
                            ),
                        ]
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
