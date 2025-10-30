import flet as ft


def main(page: ft.Page):
    def handle_item_click(e: ft.Event[ft.PopupMenuItem]):
        action = e.control.content
        page.show_dialog(
            ft.SnackBar(
                content=f"Item {action!r} selected.",
            )
        )

    page.add(
        ft.Text("Right-click or long-press the card to open a menu."),
        ft.ContextMenu(
            primary_items=[
                ft.PopupMenuItem(content="Rename", on_click=handle_item_click),
                ft.PopupMenuItem(content="Share", on_click=handle_item_click),
            ],
            primary_trigger=ft.ContextMenuTrigger.LONG_PRESS,
            secondary_items=[
                ft.PopupMenuItem(content="Copy", on_click=handle_item_click),
                ft.PopupMenuItem(content="Delete", on_click=handle_item_click),
            ],
            tertiary_items=[
                ft.PopupMenuItem(content="New tab", on_click=handle_item_click),
            ],
            on_select=lambda e: print(e),
            # on_dismiss=lambda e: page.add(ft.Text(f"{e}")),
            # on_open=lambda e: page.add(ft.Text(f"{e}")),
            expand=True,
            content=ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLUE,
                alignment=ft.Alignment.CENTER,
                border_radius=ft.BorderRadius.all(12),
                content=ft.Text("Context menu area"),
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
