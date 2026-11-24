import flet as ft
import flet_notifications as ftn


def main(page: ft.Page):
    def handle_tap(e: ftn.NotificationEvent):
        log.controls.append(ft.Text(f"Opened {e.payload}"))
        log.update()

    async def handle_action(e: ftn.NotificationActionEvent):
        message = f"{e.action_id} on {e.payload}"
        if e.input is not None:
            message += f": {e.input!r}"
        log.controls.append(ft.Text(message))
        log.update()

        # On Android, a notification the user replied to shows a progress spinner until
        # the app updates it. Our "Reply" action sets `cancel_notification=False`, so
        # this happens on every Android version (Android 16 and later wouldn't dismiss
        # it anyway). Showing the notification again with the same ID ends the spinner
        # and shows the sent reply, and `only_alert_once` keeps that update silent.
        # Other platforms dismiss the notification themselves after a reply.
        if (
            page.platform == ft.PagePlatform.ANDROID
            and e.action_id == "reply"
            and e.id is not None
        ):
            await notifications.show(
                id=e.id,
                title="Ada",
                body=f"You: {e.input}",
                payload=e.payload,
                options=ftn.NotificationOptions(
                    android=ftn.AndroidOptions(only_alert_once=True)
                ),
            )

    notifications = ftn.Notifications(on_tap=handle_tap, on_action=handle_action)

    async def show_message(e: ft.Event[ft.Button]):
        if not await notifications.request_permissions():
            page.show_dialog(ft.SnackBar("Notifications are turned off."))
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
                    cancel_notification=False,
                ),
                ftn.NotificationAction(
                    id="archive",
                    title="Archive",
                    foreground=False,  # Handled without opening the app
                ),
                ftn.NotificationAction(
                    id="delete",
                    title="Delete",
                    destructive=True,
                    require_authentication=True,
                ),
            ],
        )

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    ft.Button("Show message", on_click=show_message),
                    log := ft.Column(),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
