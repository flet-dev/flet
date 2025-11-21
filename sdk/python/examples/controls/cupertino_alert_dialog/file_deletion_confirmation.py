import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def handle_dialog_dismissal(e: ft.Event[ft.DialogControl]):
        page.add(ft.Text("Dialog dismissed"))

    def handle_action_click(e: ft.Event[ft.CupertinoDialogAction]):
        page.add(ft.Text(f"Action clicked: {e.control.content}"))
        page.pop_dialog()

    cupertino_alert_dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Cupertino Alert Dialog"),
        content=ft.Text("Do you want to delete this file?"),
        on_dismiss=handle_dialog_dismissal,
        actions=[
            ft.CupertinoDialogAction(
                content="Yes",
                destructive=True,
                on_click=handle_action_click,
            ),
            ft.CupertinoDialogAction(
                content="No", default=True, on_click=handle_action_click
            ),
        ],
    )

    page.add(
        ft.CupertinoFilledButton(
            content="Open CupertinoAlertDialog",
            on_click=lambda e: page.show_dialog(cupertino_alert_dialog),
        )
    )


ft.run(main)
