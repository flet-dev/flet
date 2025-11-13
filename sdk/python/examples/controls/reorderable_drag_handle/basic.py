import flet as ft


def main(page: ft.Page):
    def on_reorder(e: ft.OnReorderEvent):
        e.control.controls.insert(e.new_index, e.control.controls.pop(e.old_index))

    page.add(
        ft.ReorderableListView(
            expand=True,
            show_default_drag_handles=False,
            on_reorder=on_reorder,
            controls=[
                ft.ListTile(
                    title=ft.Text(f"Draggable Item {i}", color=ft.Colors.BLACK),
                    leading=ft.ReorderableDragHandle(
                        content=ft.Icon(ft.Icons.DRAG_INDICATOR, color=ft.Colors.RED),
                        mouse_cursor=ft.MouseCursor.GRAB,
                    ),
                    bgcolor=ft.Colors.ERROR
                    if i % 2 == 0
                    else ft.Colors.ON_ERROR_CONTAINER,
                )
                for i in range(10)
            ],
        )
    )


ft.run(main)
