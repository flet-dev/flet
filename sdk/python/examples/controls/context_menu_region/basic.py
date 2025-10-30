import flet as ft


def main(page: ft.Page):
    def handle_select(e: ft.ContextMenuEvent):
        item_label = e.item_control_id or e.item_key or e.item_index
        page.show_dialog(
            ft.SnackBar(
                content=f"{e.button} button selected item {item_label}.",
                duration=ft.Duration(seconds=4),
            )
        )
        page.add(ft.Text(f"{e}"))
        print(e.item)

    page.add(
        ft.Column(
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Right-click the card to open the menu."),
                ft.ContextMenuRegion(
                    primary_items=[
                        ft.PopupMenuItem(content="Rename"),
                        ft.PopupMenuItem(content="Share"),
                    ],
                    primary_trigger=ft.ContextMenuTrigger.LONG_PRESS,
                    secondary_items=[
                        ft.PopupMenuItem(content="Copy"),
                        ft.PopupMenuItem(content="Delete"),
                    ],
                    tertiary_items=[
                        ft.PopupMenuItem(content="Open in new tab"),
                    ],
                    on_select=handle_select,
                    on_dismiss=lambda e: page.add(ft.Text(f"{e}")),
                    on_request=lambda e: page.add(ft.Text(f"{e}")),
                    on_open=lambda e: page.add(ft.Text(f"{e}")),
                    content=ft.Container(
                        width=220,
                        height=120,
                        bgcolor=ft.Colors.BLUE,
                        alignment=ft.Alignment.CENTER,
                        border_radius=ft.BorderRadius.all(12),
                        content=ft.Text("Context menu area"),
                    ),
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
