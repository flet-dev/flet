import flet as ft

name = "CupertinoActionSheet Example"


def example():
    def show_cupertino_action_sheet(e):
        # e.control.page.overlay.append(cupertino_action_sheet)
        # cupertino_action_sheet.open = True
        # e.control.page.update()
        e.control.page.show_dialog(cupertino_action_sheet)

    def close_cupertino_action_sheet(e):
        # cupertino_action_sheet.open = False
        # e.control.page.update()
        e.control.page.pop_dialog()

    action_sheet = ft.CupertinoActionSheet(
        title=ft.Text("Title"),
        message=ft.Text("Message"),
        cancel=ft.CupertinoActionSheetAction(
            content=ft.Text("Cancel"),
            on_click=close_cupertino_action_sheet,
        ),
        actions=[
            ft.CupertinoActionSheetAction(
                content=ft.Text("Default Action"),
                default=True,
                on_click=lambda e: print("Default clicked"),
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Normal Action"),
                on_click=lambda e: print("Normal Action clicked"),
            ),
            ft.CupertinoActionSheetAction(
                content=ft.Text("Destructive Action"),
                destructive=True,
                on_click=lambda e: print("Destructive Action clicked"),
            ),
        ],
    )

    cupertino_action_sheet = ft.CupertinoBottomSheet(action_sheet)

    return ft.OutlinedButton(
        "Open CupertinoBottomSheet containing CupertinoActionSheet",
        on_click=show_cupertino_action_sheet,
    )
