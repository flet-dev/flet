import flet as ft


def main(page: ft.Page):
    def get_color(index: int) -> ft.Colors:
        return ft.Colors.ERROR if index % 2 == 0 else ft.Colors.ON_ERROR_CONTAINER

    def on_reorder(e: ft.OnReorderEvent):
        e.control.controls.insert(e.new_index, e.control.controls.pop(e.old_index))

    page.add(
        ft.ReorderableListView(
            expand=True,
            show_default_drag_handles=False,
            on_reorder=on_reorder,
            controls=[
                ft.ReorderableDraggable(
                    content=ft.ListTile(
                        title=ft.Text(f"Draggable Item {i}", color=ft.Colors.BLACK),
                        leading=ft.Icon(ft.Icons.CHECK, color=ft.Colors.RED),
                        bgcolor=get_color(i),
                    ),
                )
                for i in range(10)
            ],
        )
    )


ft.run(main)
