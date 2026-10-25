import flet as ft
import flet_notifications as ftn


def main(page: ft.Page):
    def handle_tap(e: ftn.NotificationEvent):
        page.show_dialog(ft.SnackBar(ft.Text(f"Opened notification {e.payload}")))

    notifications = ftn.Notifications(on_tap=handle_tap)

    async def notify(e: ft.Event[ft.Button]):
        if not await notifications.request_permissions():
            page.show_dialog(ft.SnackBar("Notifications are turned off."))
            return
        await notifications.show(
            id=1,
            title="Notification Title",
            body="This is the notification body...",
            payload="notif-1",
        )

    page.add(ft.SafeArea(content=ft.Button("Notify", on_click=notify)))


if __name__ == "__main__":
    ft.run(main)
