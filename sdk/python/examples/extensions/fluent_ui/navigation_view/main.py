import flet_fluent_ui as fluent

import flet as ft


def page_for(title: str, text: str) -> fluent.ScaffoldPage:
    return fluent.ScaffoldPage(
        header=fluent.PageHeader(title=title),
        content=ft.Text(text),
    )


def main(page: ft.Page):
    page.title = "Fluent NavigationView"
    page.padding = 0

    page.add(
        fluent.NavigationView(
            expand=True,
            selected_index=0,
            header="Mail",
            items=[
                fluent.PaneItem(
                    "Inbox",
                    icon=fluent.FluentIcons.MAIL_INBOX,
                    info_badge=fluent.InfoBadge("3"),
                    content=page_for("Inbox", "You have 3 unread messages."),
                ),
                fluent.PaneItem(
                    "Sent",
                    icon=fluent.FluentIcons.SEND,
                    content=page_for("Sent", "Messages you sent."),
                ),
                fluent.PaneItemSeparator(),
                fluent.PaneItemHeader("Folders"),
                fluent.PaneItem(
                    "Archive",
                    icon=fluent.FluentIcons.ARCHIVE,
                    content=page_for("Archive", "Archived messages."),
                ),
            ],
            footer_items=[
                fluent.PaneItem(
                    "Settings",
                    icon=fluent.FluentIcons.SETTINGS,
                    content=page_for("Settings", "Mail settings."),
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
