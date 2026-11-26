import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent ContextMenu"

    def handle_click(e: ft.Event[fluent.MenuFlyoutItem]):
        status.value = f"{e.control.content}: Report.docx"

    status = ft.Text("Right-click the file")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.ContextMenu(
                        key="file",
                        content=ft.Container(
                            width=260,
                            padding=12,
                            border_radius=4,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            content=ft.Row(
                                controls=[
                                    ft.Icon(fluent.FluentIcons.DOCUMENT),
                                    ft.Text("Report.docx"),
                                ],
                            ),
                        ),
                        items=[
                            fluent.MenuFlyoutItem(
                                "Open",
                                leading=fluent.FluentIcons.WINDOW_NEW,
                                on_click=handle_click,
                            ),
                            fluent.MenuFlyoutItem(
                                "Rename",
                                leading=fluent.FluentIcons.RENAME,
                                trailing="F2",
                                on_click=handle_click,
                            ),
                            fluent.MenuFlyoutItem(
                                "Share",
                                leading=fluent.FluentIcons.SHARE,
                                items=[
                                    fluent.MenuFlyoutItem(
                                        "Email", on_click=handle_click
                                    ),
                                    fluent.MenuFlyoutItem(
                                        "Copy link", on_click=handle_click
                                    ),
                                ],
                            ),
                            fluent.MenuFlyoutSeparator(),
                            fluent.MenuFlyoutItem(
                                "Delete",
                                leading=fluent.FluentIcons.DELETE,
                                trailing="Del",
                                on_click=handle_click,
                            ),
                        ],
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
