import flet as ft

def main(page: ft.Page):
    page.title = "AppBar Example"

    def handle_checked_item_click(e: ft.Event[ft.PopupMenuItem]):
        e.control.checked = not e.control.checked
        page.update()

    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.Icons.PALETTE),
        leading_width=40,
        title=ft.Text("AppBar Example"),
        center_title=False,
        bgcolor=ft.Colors.BLUE_GREY_400,
        actions=[
            ft.IconButton(ft.Icons.WB_SUNNY_OUTLINED),
            ft.IconButton(ft.Icons.FILTER_3),
            ft.PopupMenuButton(
                items=[
                    ft.PopupMenuItem(content="Item 1"),
                    ft.PopupMenuItem(),  # divider
                    ft.PopupMenuItem(
                        content="Checked item",
                        checked=False,
                        on_click=handle_checked_item_click,
                    ),
                ]
            ),
        ],
    )
    page.add(ft.Text("Body!"))


if __name__ == "__main__":
    ft.run(main)
