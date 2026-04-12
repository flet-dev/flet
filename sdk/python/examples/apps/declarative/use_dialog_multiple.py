import asyncio

import flet as ft


def build_rename_dialog(current_name, new_name, on_name_change, on_save, on_cancel):
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Rename {current_name}"),
        content=ft.TextField(
            label="New name",
            value=new_name,
            on_change=on_name_change,
            autofocus=True,
        ),
        actions=[
            ft.FilledButton("Save", on_click=on_save),
            ft.TextButton("Cancel", on_click=on_cancel),
        ],
    )


def build_delete_dialog(item_name, deleting, on_delete, on_cancel):
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(f"Delete {item_name}?"),
        content=ft.Text(
            "Deleting, please wait..." if deleting else "This action cannot be undone."
        ),
        actions=[
            ft.Button(
                "Deleting..." if deleting else "Delete",
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.RED if not deleting else ft.Colors.GREY,
                disabled=deleting,
                on_click=on_delete,
            ),
            ft.TextButton("Cancel", on_click=on_cancel, disabled=deleting),
        ],
    )


@ft.component
def FileItem(name, on_rename, on_delete):
    return ft.Card(
        content=ft.Container(
            padding=20,
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.DESCRIPTION),
                    ft.Text(name, size=16, expand=True),
                    ft.IconButton(
                        ft.Icons.EDIT,
                        tooltip="Rename",
                        on_click=on_rename,
                    ),
                    ft.IconButton(
                        ft.Icons.DELETE,
                        tooltip="Delete",
                        icon_color=ft.Colors.RED,
                        on_click=on_delete,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
        ),
    )


INITIAL_FILES = ["report.pdf", "photo.jpg", "notes.txt"]


@ft.component
def App():
    files, set_files = ft.use_state(INITIAL_FILES)
    target, set_target = ft.use_state(None)  # file being acted on
    new_name, set_new_name = ft.use_state("")
    show_rename, set_show_rename = ft.use_state(False)
    show_delete, set_show_delete = ft.use_state(False)
    deleting, set_deleting = ft.use_state(False)

    async def handle_delete():
        set_deleting(True)
        await asyncio.sleep(1)
        set_files([f for f in files if f != target])
        set_deleting(False)
        set_show_delete(False)

    def handle_rename_save():
        if new_name.strip():
            set_files([new_name.strip() if f == target else f for f in files])
        set_show_rename(False)

    def open_rename(name):
        def handler():
            set_target(name)
            set_new_name(name)
            set_show_rename(True)

        return handler

    def open_delete(name):
        def handler():
            set_target(name)
            set_show_delete(True)

        return handler

    ft.use_dialog(
        build_rename_dialog(
            target,
            new_name,
            on_name_change=lambda e: set_new_name(e.control.value),
            on_save=handle_rename_save,
            on_cancel=lambda: set_show_rename(False),
        )
        if show_rename
        else None
    )

    ft.use_dialog(
        build_delete_dialog(
            target,
            deleting,
            on_delete=handle_delete,
            on_cancel=lambda: set_show_delete(False),
        )
        if show_delete
        else None
    )

    return ft.Column(
        controls=[
            ft.Text("Multiple Dialogs Example", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Each file can be renamed or deleted."),
        ]
        + [
            FileItem(
                name=f,
                on_rename=open_rename(f),
                on_delete=open_delete(f),
            )
            for f in files
        ],
    )


ft.run(lambda page: page.render(App))
