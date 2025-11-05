import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    def handle_select(e: ft.ContextMenuSelectEvent):
        action = e.item.content
        page.show_dialog(ft.SnackBar(f"Item '{action}' selected."))

    async def open_menu(e: ft.Event[ft.Button]):
        await menu.open()

    page.add(
        menu := ft.ContextMenu(
            on_select=handle_select,
            content=ft.Button("Click to open menu", on_click=open_menu),
            items=[
                ft.PopupMenuItem(
                    content="Item 1",
                    on_click=lambda e: print(f"{e.control.content}"),
                ),
                ft.PopupMenuItem(
                    content="Item 2",
                    on_click=lambda e: print(f"{e.control.content}"),
                ),
                ft.PopupMenuItem(
                    content="Item 3",
                    on_click=lambda e: print(f"{e.control.content}"),
                ),
            ],
        ),
    )


if __name__ == "__main__":
    ft.run(main)
