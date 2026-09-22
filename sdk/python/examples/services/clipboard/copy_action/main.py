import flet as ft


def main(page: ft.Page):
    # `action` is performed by the client while it is still handling the click.
    # That is the only moment Safari lets a page write to the clipboard, which
    # is why `Clipboard().set()` - which has to reach Python first - does
    # nothing on iOS.
    token = "flet-1234-5678"

    def handle_copied(e):
        page.show_dialog(ft.SnackBar(ft.Text("Copied to clipboard")))

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Text(f"Token: {token}", selectable=True),
                    ft.Button(
                        "Copy token",
                        icon=ft.Icons.CONTENT_COPY,
                        action=ft.CopyToClipboard(token),
                        on_click=handle_copied,
                    ),
                    ft.Divider(),
                    ft.Text(
                        "An action's arguments are fixed before the click, so "
                        "to copy something typed just now, update the action "
                        "as the text changes."
                    ),
                    note := ft.TextField(
                        label="Note",
                        value="Edit me, then copy",
                        on_change=lambda e: setattr(
                            copy_note, "action", ft.CopyToClipboard(note.value)
                        ),
                    ),
                    copy_note := ft.Button(
                        "Copy note",
                        icon=ft.Icons.CONTENT_COPY,
                        action=ft.CopyToClipboard("Edit me, then copy"),
                        on_click=handle_copied,
                    ),
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
