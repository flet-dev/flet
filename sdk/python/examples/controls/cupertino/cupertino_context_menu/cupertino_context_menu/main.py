import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.SafeArea(
            content=ft.CupertinoContextMenu(
                enable_haptic_feedback=True,
                actions=[
                    ft.CupertinoContextMenuAction(
                        default=True,
                        trailing_icon=ft.Icons.CHECK,
                        on_click=lambda _: print("Action 1"),
                        content="Action 1",
                    ),
                    ft.CupertinoContextMenuAction(
                        trailing_icon=ft.Icons.MORE,
                        on_click=lambda _: print("Action 2"),
                        content="Action 2",
                    ),
                    ft.CupertinoContextMenuAction(
                        destructive=True,
                        trailing_icon=ft.Icons.CANCEL,
                        on_click=lambda _: print("Action 3"),
                        content="Action 3",
                    ),
                ],
                content=ft.Image("https://picsum.photos/200/200"),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
