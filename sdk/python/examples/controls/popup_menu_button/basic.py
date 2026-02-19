import flet as ft


def main(page: ft.Page):
    def handle_check_item_click(e: ft.Event[ft.PopupMenuItem]):
        e.control.checked = not e.control.checked
        page.update()

    page.add(
        ft.PopupMenuButton(
            key="popup",
            items=[
                ft.PopupMenuItem(content="Item 1"),
                ft.PopupMenuItem(icon=ft.Icons.POWER_INPUT, content="Check power"),
                ft.PopupMenuItem(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.HOURGLASS_TOP_OUTLINED),
                            ft.Text("Item with a custom content"),
                        ]
                    ),
                    on_click=lambda _: print("Button with custom content clicked!"),
                ),
                ft.PopupMenuItem(),  # divider
                ft.PopupMenuItem(
                    content="Checked item",
                    checked=False,
                    on_click=handle_check_item_click,
                ),
            ],
        )
    )


if __name__ == "__main__":
    ft.run(main)
