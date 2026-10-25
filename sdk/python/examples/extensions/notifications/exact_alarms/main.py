from datetime import timedelta

import flet as ft
import flet_notifications as ftn


async def main(page: ft.Page):
    if page.web or page.platform not in {
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.ANDROID_TV,
    }:
        page.add(
            ft.SafeArea(
                content=ft.Text(
                    "Exact alarms are an Android permission. Other platforms "
                    "deliver scheduled notifications on time without it."
                )
            )
        )
        return

    notifications = ftn.Notifications()

    async def refresh():
        allowed = await notifications.can_schedule_exact_alarms()
        status.value = (
            "Exact alarms are allowed." if allowed else "Exact alarms are not allowed."
        )
        allow_button.visible = not allowed
        page.update()

    async def allow(e: ft.Event[ft.Button]):
        # Opens the system's "Alarms & reminders" page for this app.
        await notifications.request_exact_alarm_permission()

    async def schedule(e: ft.Event[ft.Button]):
        if not await notifications.can_schedule_exact_alarms():
            page.show_dialog(ft.SnackBar(ft.Text("Allow exact alarms first.")))
            return
        await notifications.request_permissions()
        await notifications.schedule(
            1,
            when=timedelta(minutes=1),
            title="One minute is up",
            body="Delivered on the dot, even in Doze.",
            schedule_mode=ftn.AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
        )
        page.show_dialog(ft.SnackBar(ft.Text("Scheduled for one minute from now.")))

    async def handle_lifecycle(e: ft.AppLifecycleStateChangeEvent):
        if e.state == ft.AppLifecycleState.RESUME:
            await refresh()

    page.on_app_lifecycle_state_change = handle_lifecycle
    status = ft.Text()
    allow_button = ft.Button("Allow exact alarms", on_click=allow)
    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    status,
                    allow_button,
                    ft.Button("Remind me in exactly one minute", on_click=schedule),
                ]
            )
        )
    )
    await refresh()


if __name__ == "__main__":
    ft.run(main)
