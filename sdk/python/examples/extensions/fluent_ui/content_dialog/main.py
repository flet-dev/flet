import flet_fluent_ui as fluent

import flet as ft


def main(page: ft.Page):
    page.title = "Fluent ContentDialog"

    def delete(e: ft.Event[fluent.FilledButton]):
        page.pop_dialog()
        # pop_dialog() sends its own update, so the page is not auto-updated
        # after this handler; send the status change explicitly.
        status.value = "File deleted"
        status.update()

    def cancel(e: ft.Event[fluent.Button]):
        page.pop_dialog()
        status.value = "Kept the file"
        status.update()

    dialog = fluent.ContentDialog(
        title="Delete file?",
        content="If you delete this file, you won't be able to recover it.",
        actions=[
            fluent.FilledButton("Delete", on_click=delete),
            fluent.Button("Cancel", on_click=cancel),
        ],
    )

    status = ft.Text()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    fluent.Button(
                        "Delete file", on_click=lambda e: page.show_dialog(dialog)
                    ),
                    status,
                ],
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
