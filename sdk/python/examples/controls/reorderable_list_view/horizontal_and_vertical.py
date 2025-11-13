import flet as ft


def main(page: ft.Page):
    # the primary color is the color of the reorder handle
    page.theme = page.dark_theme = ft.Theme(
        color_scheme=ft.ColorScheme(primary=ft.Colors.BLUE)
    )

    def handle_reorder(e: ft.OnReorderEvent):
        e.control.controls.insert(e.new_index, e.control.controls.pop(e.old_index))

    def get_color(i):
        return ft.Colors.ERROR if i % 2 == 0 else ft.Colors.ON_ERROR_CONTAINER

    page.add(
        # horizontal
        ft.ReorderableListView(
            expand=True,
            horizontal=True,
            on_reorder=handle_reorder,
            controls=[
                ft.Container(
                    content=ft.Text(f"Item {i}", color=ft.Colors.BLACK),
                    bgcolor=get_color(i),
                    margin=ft.Margin.symmetric(horizontal=5, vertical=10),
                    width=100,
                    alignment=ft.Alignment.CENTER,
                )
                for i in range(10)
            ],
        ),
        # vertical
        ft.ReorderableListView(
            expand=True,
            on_reorder=handle_reorder,
            controls=[
                ft.ListTile(
                    title=ft.Text(f"Item {i}", color=ft.Colors.BLACK),
                    leading=ft.Icon(ft.Icons.CHECK, color=ft.Colors.RED),
                    bgcolor=get_color(i),
                )
                for i in range(10)
            ],
        ),
    )


ft.run(main)
