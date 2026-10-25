import asyncio

import flet as ft
import flet_notifications as ftn

STEPS = 10


async def main(page: ft.Page):
    android = not page.web and page.platform in {
        ft.PagePlatform.ANDROID,
        ft.PagePlatform.ANDROID_TV,
    }
    windows = not page.web and page.platform == ft.PagePlatform.WINDOWS
    if not (android or windows):
        page.add(
            ft.SafeArea(
                content=ft.Text(
                    "Progress bars in notifications need Android or Windows. "
                    "Run this example on one of them."
                )
            )
        )
        return

    notifications = ftn.Notifications()

    async def show_android_progress(step: int):
        # Showing the same ID again updates the notification in place.
        await notifications.show(
            1,
            title="Downloading report.pdf",
            options=ftn.NotificationOptions(
                android=ftn.AndroidOptions(
                    progress=ftn.AndroidProgress(value=step, max=STEPS),
                    only_alert_once=True,
                    ongoing=True,
                )
            ),
        )

    async def download(e: ft.Event[ft.Button]):
        await notifications.request_permissions()
        if windows:
            await notifications.show(
                1,
                title="Downloading report.pdf",
                options=ftn.NotificationOptions(
                    windows=ftn.WindowsOptions(
                        # Updates change only the fields the notification was
                        # shown with, so it starts with a label too.
                        progress=ftn.WindowsProgress(
                            status="Downloading", max=STEPS, label=f"0/{STEPS}"
                        )
                    )
                ),
            )
        for step in range(1, STEPS + 1):
            await asyncio.sleep(0.5)
            if android:
                await show_android_progress(step)
            elif not await notifications.update_windows_progress(
                1,
                ftn.WindowsProgress(
                    status="Downloading", value=step, max=STEPS, label=f"{step}/{STEPS}"
                ),
            ):
                page.show_dialog(ft.SnackBar(ft.Text("Download notification closed.")))
                return
        await notifications.show(1, title="report.pdf", body="Download complete")

    page.add(ft.SafeArea(content=ft.Button("Download", on_click=download)))


if __name__ == "__main__":
    ft.run(main)
