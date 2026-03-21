import asyncio

import flet as ft


@ft.component
def App():
    show, set_show = ft.use_state(False)
    deleting, set_deleting = ft.use_state(False)

    async def handle_delete():
        set_deleting(True)
        # Simulate async operation
        await asyncio.sleep(2)
        set_deleting(False)
        set_show(False)

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
                    on_click=lambda: set_show(False),
                    disabled=deleting,
                ),
            ],
            on_dismiss=lambda: set_show(False),
        )
        if show
        else None
    )

    return ft.Column(
        controls=[
            ft.Text("Declarative Dialog Example", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Click the button to open a confirmation dialog."),
            ft.Button(
                "Delete File",
                icon=ft.Icons.DELETE,
                on_click=lambda: set_show(True),
            ),
        ],
    )


ft.run(lambda page: page.render(App))
