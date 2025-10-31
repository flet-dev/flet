import flet as ft


async def main(page: ft.Page):
    # on web, disable default browser context menu
    if page.web:
        await page.browser_context_menu.disable()

    def handle_item_click(e: ft.Event[ft.PopupMenuItem]):
        action = e.control.content
        page.show_dialog(ft.SnackBar(content=f"Item '{action}' selected."))

    page.add(
        ft.ContextMenu(
            primary_items=[
                ft.PopupMenuItem(content="Primary 1", on_click=handle_item_click),
                ft.PopupMenuItem(content="Primary 2", on_click=handle_item_click),
            ],
            primary_trigger=ft.ContextMenuTrigger.DOWN,
            secondary_items=[
                ft.PopupMenuItem(content="Secondary 1", on_click=handle_item_click),
                ft.PopupMenuItem(content="Secondary 2", on_click=handle_item_click),
            ],
            secondary_trigger=ft.ContextMenuTrigger.DOWN,
            tertiary_items=[
                ft.PopupMenuItem(content="Tertiary 1", on_click=handle_item_click),
                ft.PopupMenuItem(content="Tertiary 2", on_click=handle_item_click),
            ],
            tertiary_trigger=ft.ContextMenuTrigger.DOWN,
            on_open=lambda e: print("Menu opened"),
            on_select=lambda e: print(f"Selected item: {e.item.content}"),
            on_dismiss=lambda e: print("Menu dismissed"),
            expand=True,
            content=ft.Container(
                expand=True,
                bgcolor=ft.Colors.BLUE,
                alignment=ft.Alignment.CENTER,
                border_radius=ft.BorderRadius.all(12),
                content=ft.Text("Left/middle/right click to open a context menu."),
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
