import flet as ft


def main(page: ft.Page):
    async def open_menu(e: ft.TapEvent[ft.GestureDetector]):
        await menu.open(
            local_position=e.local_position,
            global_position=e.global_position,
        )

    page.add(
        menu := ft.ContextMenu(
            expand=True,
            items=[
                ft.PopupMenuItem(
                    content="Cut",
                    on_click=lambda e: print(f"{e.control.content}"),
                ),
                ft.PopupMenuItem(
                    content="Copy",
                    on_click=lambda e: print(f"{e.control.content}"),
                ),
                ft.PopupMenuItem(
                    content="Paste",
                    on_click=lambda e: print(f"{e.control.content}"),
                ),
            ],
            content=ft.GestureDetector(
                expand=True,
                on_double_tap_down=open_menu,
                content=ft.Container(
                    content=ft.Text("Double-click to open the context menu."),
                    bgcolor=ft.Colors.BLUE,
                    alignment=ft.Alignment.CENTER,
                ),
            ),
        ),
    )


if __name__ == "__main__":
    ft.run(main)
