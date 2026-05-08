import flet as ft


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    messages = ft.Column(tight=True)

    def handle_dialog_dismissal(_: ft.Event[ft.DialogControl]):
        messages.controls.append(ft.Text("Dialog dismissed"))

    def handle_action_click(e: ft.Event[ft.CupertinoDialogAction]):
        messages.controls.append(ft.Text(f"Action clicked: {e.control.content}"))
        page.pop_dialog()

    cupertino_alert_dialog = ft.CupertinoAlertDialog(
        title=ft.Text("Cupertino Alert Dialog"),
        content=ft.Text("Do you want to delete this file?"),
        on_dismiss=handle_dialog_dismissal,
        actions=[
            ft.CupertinoDialogAction(
                destructive=True,
                on_click=handle_action_click,
                content="Yes",
            ),
            ft.CupertinoDialogAction(
                default=True,
                on_click=handle_action_click,
                content="No",
            ),
        ],
    )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.CupertinoFilledButton(
                        on_click=lambda _: page.show_dialog(cupertino_alert_dialog),
                        content="Open CupertinoAlertDialog",
                    ),
                    messages,
                ],
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
