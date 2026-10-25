import flet as ft
import flet_notifications as ftn

GROUP = "chat"
CHANNELS = [
    ftn.NotificationChannel(
        id="messages",
        name="Messages",
        description="New direct messages",
        group_id=GROUP,
        importance=ftn.AndroidImportance.HIGH,
    ),
    ftn.NotificationChannel(
        id="digest",
        name="Daily digest",
        description="A quiet summary once a day",
        group_id=GROUP,
        importance=ftn.AndroidImportance.LOW,
        play_sound=False,
        enable_vibration=False,
    ),
]


async def main(page: ft.Page):
    if page.web or page.platform not in {
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.ANDROID_TV,
    }:
        page.add(
            ft.SafeArea(
                content=ft.Text(
                    "Notification channels exist only on Android. "
                    "Run this example on Android."
                )
            )
        )
        return

    notifications = ftn.Notifications()

    async def refresh():
        channels = await notifications.get_notification_channels()
        listed.controls = [
            ft.Text(f"{c.name} ({c.importance.name.lower()})") for c in channels
        ] or [ft.Text("No channels yet.")]
        # Android drops notifications posted to a channel that doesn't exist.
        post_button.disabled = "messages" not in {c.id for c in channels}
        page.update()

    async def create(e: ft.Event[ft.Button]):
        await notifications.create_notification_channel_group(GROUP, name="Chat")
        for channel in CHANNELS:
            await notifications.create_notification_channel(channel)
        await refresh()

    async def post(e: ft.Event[ft.Button]):
        await notifications.request_permissions()
        await notifications.show(
            1,
            title="Ada",
            body="Are you free?",
            # The channel decides how the notification alerts.
            options=ftn.NotificationOptions(
                android=ftn.AndroidOptions(channel="messages")
            ),
        )

    async def delete(e: ft.Event[ft.Button]):
        # Deleting a group deletes its channels too.
        await notifications.delete_notification_channel_group(GROUP)
        await refresh()

    listed = ft.Column()
    post_button = ft.Button("Post a message", on_click=post)
    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    ft.Button("Create channels", on_click=create),
                    post_button,
                    ft.Button("Delete channels", on_click=delete),
                    ft.Text("Channels", weight=ft.FontWeight.BOLD),
                    listed,
                ]
            )
        )
    )
    await refresh()


if __name__ == "__main__":
    ft.run(main)
