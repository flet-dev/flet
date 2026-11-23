import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent InfoBadge"

    def mark_read(e: ft.Event[fluent.Button]):
        unread.visible = False
        status.value = "All caught up"

    unread = fluent.InfoBadge("5")
    status = ft.Text("5 unread messages")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[ft.Text("Inbox"), unread],
                    ),
                    ft.Row(
                        controls=[
                            ft.Text("Updates"),
                            fluent.InfoBadge(severity=fluent.InfoBarSeverity.ERROR),
                        ],
                    ),
                    fluent.Button("Mark all as read", on_click=mark_read),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
