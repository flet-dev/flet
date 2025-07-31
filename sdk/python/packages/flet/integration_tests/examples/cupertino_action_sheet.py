import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_click(e):
        page.add(ft.Text(f"Action clicked: {e.control.content.value}"))
        page.pop_dialog()

    action_sheet = ft.CupertinoActionSheet(
        key=456,
        title=ft.Row(
            controls=[ft.Text("Title"), ft.Icon(ft.Icons.BEDTIME)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        message=ft.Row(
            controls=[ft.Text("Description"), ft.Icon(ft.Icons.AUTO_AWESOME)],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        cancel=ft.CupertinoActionSheetAction(
            content=ft.Text("Cancel"),
            on_click=handle_click,
        ),
        actions=[
            ft.CupertinoActionSheetAction(
                content=ft.Text("Default Action"),
                default=True,
                on_click=handle_click,
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Normal Action"),
                on_click=handle_click,
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Destructive Action"),
                destructive=True,
                on_click=handle_click,
            ),
        ],
    )

    bottom_sheet = ft.CupertinoBottomSheet(action_sheet)

    page.add(
        ft.CupertinoFilledButton(
            key=123,
            content="Open CupertinoBottomSheet",
            on_click=lambda e: page.show_dialog(bottom_sheet),
        )
    )


ft.run(main)
