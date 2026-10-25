import flet as ft
import flet_notifications as ftn


def main(page: ft.Page):
    if page.web or page.platform not in {
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.ANDROID_TV,
    }:
        page.add(
            ft.SafeArea(
                content=ft.Text(
                    "Foreground services exist only on Android. "
                    "Run this example on Android."
                )
            )
        )
        return

    notifications = ftn.Notifications()

    async def start(e: ft.Event[ft.Button]):
        await notifications.request_permissions()
        await notifications.start_foreground_service(
            1,
            title="Syncing photos",
            body="Keeps running while you use other apps",
            service_types=[ftn.AndroidForegroundServiceType.DATA_SYNC],
        )

    async def stop(e: ft.Event[ft.Button]):
        await notifications.stop_foreground_service()

    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    ft.Button("Start sync", on_click=start),
                    ft.Button("Stop sync", on_click=stop),
                ]
            )
        )
    )


if __name__ == "__main__":
    ft.run(main)
