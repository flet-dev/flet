import flet as ft


def main(page: ft.Page):
    def get_color(index: int) -> ft.Colors:
        return ft.Colors.ERROR if index % 2 == 0 else ft.Colors.ON_ERROR_CONTAINER

    page.add(
        ft.ReorderableListView(
            expand=True,
            show_default_drag_handles=False,
            on_reorder=lambda e: print(
                f"Reordered from {e.old_index} to {e.new_index}"
            ),
            controls=[
                ft.ReorderableDraggable(
                    index=i,
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
