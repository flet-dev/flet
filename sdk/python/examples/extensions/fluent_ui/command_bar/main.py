import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent CommandBar"

    def handle_click(e: ft.Event[fluent.CommandBarButton]):
        status.value = f"{e.control.content} clicked"

    status = ft.Text("Pick a command")

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.CommandBar(
                        primary_items=[
                            fluent.CommandBarButton(
                                icon=fluent.FluentIcons.MAIL_REPLY,
                                content="Reply",
                                on_click=handle_click,
                            ),
                            fluent.CommandBarButton(
                                icon=fluent.FluentIcons.MAIL_FORWARD,
                                content="Forward",
                                on_click=handle_click,
                            ),
                            fluent.CommandBarSeparator(),
                            fluent.CommandBarButton(
                                icon=fluent.FluentIcons.ARCHIVE,
                                content="Archive",
                                on_click=handle_click,
                            ),
                            fluent.CommandBarButton(
                                icon=fluent.FluentIcons.DELETE,
                                content="Delete",
                                on_click=handle_click,
                            ),
                        ],
                        secondary_items=[
                            fluent.CommandBarButton(
                                icon=fluent.FluentIcons.FLAG,
                                content="Flag",
                                on_click=handle_click,
                            ),
                            fluent.CommandBarButton(
                                icon=fluent.FluentIcons.READ,
                                content="Mark as read",
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
