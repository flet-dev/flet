import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.CupertinoContextMenu(
            enable_haptic_feedback=True,
            content=ft.Image("https://picsum.photos/200/200"),
            actions=[
                ft.CupertinoContextMenuAction(
                    content="Action 1",
                    default=True,
                    trailing_icon=ft.Icons.CHECK,
                    on_click=lambda e: print("Action 1"),
                ),
                ft.CupertinoContextMenuAction(
                    content="Action 2",
                    trailing_icon=ft.Icons.MORE,
                    on_click=lambda e: print("Action 2"),
                ),
                ft.CupertinoContextMenuAction(
                    content="Action 3",
                    destructive=True,
                    trailing_icon=ft.Icons.CANCEL,
                    on_click=lambda e: print("Action 3"),
                ),
            ],
        )
    )


ft.run(main)
