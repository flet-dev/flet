import flet as ft
import flet_notifications as ftn


def main(page: ft.Page):
    def handle_tap(e: ftn.NotificationEvent):
        log.controls.append(ft.Text(f"Opened {e.payload}"))
        log.update()

    def handle_action(e: ftn.NotificationActionEvent):
        message = f"{e.action_id} on {e.payload}"
        if e.input is not None:
            message += f": {e.input!r}"
        log.controls.append(ft.Text(message))
        log.update()

    notifications = ftn.Notifications(on_tap=handle_tap, on_action=handle_action)

    async def show_message(e: ft.Event[ft.Button]):
        if not await notifications.request_permissions():
            page.show_dialog(ft.SnackBar(ft.Text("Notifications are turned off.")))
            return
        await notifications.show(
            id=1,
            title="Ada",
            body="Lunch at noon?",
            payload="chat:ada",
            actions=[
                ftn.NotificationAction(
                    id="reply",
                    title="Reply",
                    input=ftn.NotificationActionInput(label="Message"),
                ),
                # Handled without opening the app.
                ftn.NotificationAction(id="archive", title="Archive", foreground=False),
                ftn.NotificationAction(
                    id="delete",
                    title="Delete",
                    destructive=True,
                    require_authentication=True,
                ),
            ],
        )

    log = ft.Column()
    page.add(
        ft.SafeArea(
            content=ft.Column([ft.Button("Show message", on_click=show_message), log])
        )
    )


if __name__ == "__main__":
    ft.run(main)
