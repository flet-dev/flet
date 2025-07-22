import flet as ft


def main(page: ft.Page):
    get_color = lambda i: (
        ft.Colors.ERROR if i % 2 == 0 else ft.Colors.ON_ERROR_CONTAINER
    )

    page.add(
        ft.ReorderableListView(
            expand=True,
            build_controls_on_demand=False,
            on_reorder=lambda e: print(
                f"Reordered from {e.old_index} to {e.new_index}"
            ),
            show_default_drag_handles=True,
            controls=[
                ft.ReorderableDraggable(
                    index=i,
                    content=ft.ListTile(
                        title=ft.Text(f"Item {i}", color=ft.Colors.BLACK),
                        leading=ft.Icon(ft.Icons.CHECK, color=ft.Colors.RED),
                        bgcolor=get_color(i),
                    ),
                )
                for i in range(10)
            ],
        )
    )


ft.app(main)
