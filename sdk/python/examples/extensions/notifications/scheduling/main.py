from datetime import datetime, time, timedelta

import flet as ft
import flet_notifications as ftn

SUPPORTED = {
    ft.PagePlatform.ANDROID,
    ft.PagePlatform.ANDROID_TV,
    ft.PagePlatform.IOS,
    ft.PagePlatform.MACOS,
    ft.PagePlatform.WINDOWS,
}


async def main(page: ft.Page):
    if page.web or page.platform not in SUPPORTED:
        page.add(
            ft.SafeArea(
                content=ft.Text(
                    "Scheduling needs Android, iOS, macOS or Windows. "
                    "Run this example on one of them."
                )
            )
        )
        return

    notifications = ftn.Notifications()
    # Windows schedules one-off notifications only, without recurrence.
    windows = page.platform == ft.PagePlatform.WINDOWS

    async def refresh():
        scheduled = await notifications.get_pending_notifications()
        # Windows reports pending notifications without their title.
        rows = [ft.Text(f"#{n.id} {n.title or ''}") for n in scheduled]
        pending.controls = rows or [ft.Text("Nothing scheduled.")]
        page.update()

    async def in_ten_seconds(e: ft.Event[ft.Button]):
        await notifications.request_permissions()
        await notifications.schedule(
            1, when=timedelta(seconds=10), title="Stretch", body="Time to stand up."
        )
        await refresh()

    async def every_morning(e: ft.Event[ft.Button]):
        await notifications.request_permissions()
        # A naive datetime is device time, so this follows the user across zones.
        next_nine = datetime.combine(datetime.now().date(), time(9))
        if next_nine < datetime.now():
            next_nine += timedelta(days=1)
        await notifications.schedule(
            2,
            when=next_nine,
            title="Good morning",
            body="Here is your daily summary.",
            match_components=ftn.DateTimeComponents.TIME,
        )
        await refresh()

    async def every_hour(e: ft.Event[ft.Button]):
        await notifications.request_permissions()
        await notifications.periodically_show(
            3,
            repeat_interval=ftn.RepeatInterval.HOURLY,
            title="Hourly check-in",
            body="How is it going?",
        )
        await refresh()

    async def cancel_all(e: ft.Event[ft.Button]):
        await notifications.cancel_all_pending()
        await refresh()

    pending = ft.Column()
    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    ft.Button("In 10 seconds", on_click=in_ten_seconds),
                    ft.Button(
                        "Every day at 9:00", on_click=every_morning, visible=not windows
                    ),
                    ft.Button("Every hour", on_click=every_hour, visible=not windows),
                    ft.Button("Cancel all", on_click=cancel_all, visible=not windows),
                    ft.Text("Pending", weight=ft.FontWeight.BOLD),
                    pending,
                ]
            )
        )
    )
    await refresh()


if __name__ == "__main__":
    ft.run(main)
