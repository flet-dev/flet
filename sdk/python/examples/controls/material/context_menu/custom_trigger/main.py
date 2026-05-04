import flet as ft


def main(page: ft.Page):
    async def open_menu(e: ft.TapEvent[ft.GestureDetector]):
        await menu.open(
            local_position=e.local_position,
            global_position=e.global_position,
        )

    menu = ft.ContextMenu(
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
                key="context_menu_custom_trigger_area",
                bgcolor=ft.Colors.BLUE,
                alignment=ft.Alignment.CENTER,
                content=ft.Text("Double-click to open the context menu."),
            ),
        ),
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=menu,
        ),
    )


if __name__ == "__main__":
    ft.run(main)
