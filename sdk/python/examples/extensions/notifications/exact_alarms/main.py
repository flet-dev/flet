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
        allow_button.disabled = allowed
        allow_button.tooltip = "Already allowed" if allowed else None
        page.update()

    async def allow(e: ft.Event[ft.Button]):
        # Opens the system's "Alarms & reminders" page for this app.
        await notifications.request_exact_alarm_permission()

    async def schedule(e: ft.Event[ft.Button]):
        if not await notifications.can_schedule_exact_alarms():
            page.show_dialog(ft.SnackBar("Allow exact alarms first."))
            return
        await notifications.request_permissions()
        await notifications.schedule(
            1,
            when=timedelta(minutes=1),
            title="One minute is up",
            body="Delivered on the dot, even in Doze.",
            schedule_mode=ftn.AndroidScheduleMode.EXACT_ALLOW_WHILE_IDLE,
        )
        page.show_dialog(ft.SnackBar("Scheduled for one minute from now."))

    async def handle_lifecycle(e: ft.AppLifecycleStateChangeEvent):
        if e.state == ft.AppLifecycleState.RESUME:
            await refresh()

    page.on_app_lifecycle_state_change = handle_lifecycle

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    status := ft.Text(),
                    allow_button := ft.Button("Allow exact alarms", on_click=allow),
                    ft.Button("Remind me in exactly one minute", on_click=schedule),
                ]
            )
        )
    )
    await refresh()


if __name__ == "__main__":
    ft.run(main)
