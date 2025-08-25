import flet as ft

name = "CupertinoAlertDialog example"


def example():
    def dismiss_dialog(e):
        e.control.page.pop_dialog()

    cupertino_alert_dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Cupertino Alert Dialog"),
        content=ft.Text("Do you want to delete this file?"),
        actions=[
            ft.CupertinoDialogAction("OK", destructive=True, on_click=dismiss_dialog),
            ft.CupertinoDialogAction(content="Cancel", on_click=dismiss_dialog),
        ],
    )

    def open_dlg(e):
        e.control.page.show_dialog(cupertino_alert_dialog)

    return ft.Button("Open CupertinoAlertDialog", on_click=open_dlg)
