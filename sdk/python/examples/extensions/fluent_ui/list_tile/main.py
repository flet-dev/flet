import flet_fluent_ui as fluent

import flet as ft

FOLDERS = [
    ("Inbox", fluent.FluentIcons.INBOX, "3 unread"),
    ("Sent", fluent.FluentIcons.SEND, None),
    ("Archive", fluent.FluentIcons.ARCHIVE, None),
]


def main(page: ft.Page):
    page.title = "Fluent ListTile"

    def handle_select(e: ft.Event[fluent.ListTile]):
        # Single selection: deselect the other folders.
        for tile in tiles:
            tile.selected = tile is e.control
        status.value = f"Folder: {e.control.title}"

    tiles = [
        fluent.ListTile(
            title=name,
            subtitle=subtitle,
            leading=icon,
            selection_mode=fluent.ListTileSelectionMode.SINGLE,
            selected=name == "Inbox",
            on_selection_change=handle_select,
        )
        for name, icon, subtitle in FOLDERS
    ]
    status = ft.Text("Folder: Inbox")

    page.add(
        ft.SafeArea(
            content=ft.Column(width=280, controls=[*tiles, status]),
        )
    )


if __name__ == "__main__":
    ft.run(main)
