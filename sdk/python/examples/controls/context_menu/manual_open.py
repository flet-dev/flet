import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def handle_select(e: ft.ContextMenuSelectEvent):
        action = e.item.content
        page.show_dialog(ft.SnackBar(content=f"Item '{action}' selected."))

    async def open_menu(e: ft.Event[ft.Button]):
        await context_menu.open()

    page.add(
        context_menu := ft.ContextMenu(
            on_select=handle_select,
            content=ft.Button("Open Menu", on_click=open_menu),
            items=[
                ft.PopupMenuItem(
                    content="Cut",
                    on_click=lambda e: print(f"Action '{e.control.content}' clicked!"),
                ),
                ft.PopupMenuItem(
                    content="Copy",
                    on_click=lambda e: print(f"Action '{e.control.content}' clicked!"),
                ),
                ft.PopupMenuItem(
                    content="Paste",
                    on_click=lambda e: print(f"Action '{e.control.content}' clicked!"),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
