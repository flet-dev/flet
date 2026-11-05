import flet as ft
import flet_notifications as ftn


async def main(page: ft.Page):
    notifications = ftn.Notifications()
    android = not page.web and page.platform in {
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.ANDROID_TV,
    }
    has_settings = not page.web and page.platform in {
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.ANDROID_TV,
        ft.PagePlatform.IOS,
        ft.PagePlatform.MACOS,
    }

    async def refresh():
        enabled = await notifications.are_notifications_enabled()
        status.value = "Notifications are on." if enabled else "Notifications are off."
        page.update()

    async def request(e: ft.Event[ft.Button]):
        await notifications.request_permissions()
        await refresh()

    async def open_settings(e: ft.Event[ft.Button]):
        await notifications.open_settings()

    async def request_full_screen(e: ft.Event[ft.Button]):
        granted = await notifications.request_full_screen_intent_permission()
        page.show_dialog(ft.SnackBar(f"Full-screen notifications: {granted}"))

    async def request_policy_access(e: ft.Event[ft.Button]):
        if not await notifications.has_notification_policy_access():
            await notifications.request_notification_policy_access()

    async def handle_lifecycle(e: ft.AppLifecycleStateChangeEvent):
        # The user may have changed the setting while the app was in the background.
        if e.state == ft.AppLifecycleState.RESUME:
            await refresh()

    page.on_app_lifecycle_state_change = handle_lifecycle

    page.add(
        ft.SafeArea(
            content=ft.Column(
                controls=[
                    status := ft.Text(),
                    ft.Button("Ask for permission", on_click=request),
                    ft.Button(
                        "Open notification settings",
                        on_click=open_settings,
                        disabled=not has_settings,
                        tooltip=None if has_settings else "Android, iOS and macOS only",
                    ),
                    ft.Button(
                        "Allow full-screen notifications",
                        on_click=request_full_screen,
                        disabled=not android,
                        tooltip=None if android else "Android only",
                    ),
                    ft.Button(
                        "Allow Do Not Disturb access",
                        on_click=request_policy_access,
                        disabled=not android,
                        tooltip=None if android else "Android only",
                    ),
                ]
            )
        )
    )
    await refresh()


if __name__ == "__main__":
    ft.run(main)
