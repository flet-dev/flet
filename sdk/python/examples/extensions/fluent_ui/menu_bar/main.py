import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent MenuBar"

    def handle_click(e: ft.Event[fluent.MenuFlyoutItem]):
        status.value = f"{e.control.content} clicked"

    def toggle_status_bar(e: ft.Event[fluent.ToggleMenuFlyoutItem]):
        status.visible = e.control.value

    status = ft.Text("Pick a command")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.MenuBar(
                        items=[
                            fluent.MenuBarItem(
                                "File",
                                items=[
                                    fluent.MenuFlyoutItem(
                                        "New",
                                        trailing="Ctrl+N",
                                        on_click=handle_click,
                                    ),
                                    fluent.MenuFlyoutItem(
                                        "Open...",
                                        trailing="Ctrl+O",
                                        on_click=handle_click,
                                    ),
                                    fluent.MenuFlyoutItem(
                                        "Save",
                                        trailing="Ctrl+S",
                                        on_click=handle_click,
                                    ),
                                ],
                            ),
                            fluent.MenuBarItem(
                                "Edit",
                                items=[
                                    fluent.MenuFlyoutItem(
                                        "Undo",
                                        trailing="Ctrl+Z",
                                        on_click=handle_click,
                                    ),
                                    fluent.MenuFlyoutSeparator(),
                                    fluent.MenuFlyoutItem(
                                        "Cut",
                                        trailing="Ctrl+X",
                                        on_click=handle_click,
                                    ),
                                    fluent.MenuFlyoutItem(
                                        "Copy",
                                        trailing="Ctrl+C",
                                        on_click=handle_click,
                                    ),
                                    fluent.MenuFlyoutItem(
                                        "Paste",
                                        trailing="Ctrl+V",
                                        on_click=handle_click,
                                    ),
                                ],
                            ),
                            fluent.MenuBarItem(
                                "View",
                                items=[
                                    fluent.ToggleMenuFlyoutItem(
                                        "Status bar",
                                        value=True,
                                        on_change=toggle_status_bar,
                                    ),
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
