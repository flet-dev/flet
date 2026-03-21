import asyncio

import flet as ft


@ft.component
def App():
    show_confirm, set_show_confirm = ft.use_state(False)
    show_success, set_show_success = ft.use_state(False)
    deleting, set_deleting = ft.use_state(False)
    deleted, set_deleted = ft.use_state(False)
    # Ref avoids stale closure — always holds the current value
    should_chain = ft.use_ref(False)

    async def handle_delete(e):
        set_deleting(True)
        await asyncio.sleep(2)
        set_deleting(False)
        set_deleted(True)
        should_chain.current = True
        set_show_confirm(False)

    def on_confirm_dismiss(e):
        if should_chain.current:
            should_chain.current = False
            set_show_success(True)

    ft.use_dialog(
        ft.AlertDialog(
            modal=True,
            title=ft.Text("Delete report.pdf?"),
            content=ft.Text(
                "Deleting, please wait..." if deleting else "This cannot be undone."
            ),
            actions=[
                ft.Button(
                    "Deleting..." if deleting else "Delete",
                    disabled=deleting,
                    on_click=handle_delete,
                ),
                ft.TextButton(
                    "Cancel",
                    on_click=lambda e: set_show_confirm(False),
                    disabled=deleting,
                ),
            ],
            on_dismiss=on_confirm_dismiss,
        )
        if show_confirm
        else None
    )

    ft.use_dialog(
        ft.AlertDialog(
            title=ft.Text("Done!"),
            content=ft.Text("report.pdf has been deleted."),
            actions=[
                ft.FilledButton("OK", on_click=lambda e: set_show_success(False)),
            ],
        )
        if show_success
        else None
    )

    return ft.Column(
        controls=[
            ft.Text("Chained Dialogs Example", size=24, weight=ft.FontWeight.BOLD),
            ft.Text(
                "File deleted." if deleted else "Click the button to delete the file."
            ),
            ft.Button(
                "Delete File",
                icon=ft.Icons.DELETE,
                on_click=lambda e: set_show_confirm(True),
                disabled=deleted,
            ),
        ],
    )


ft.run(lambda page: page.render(App))
