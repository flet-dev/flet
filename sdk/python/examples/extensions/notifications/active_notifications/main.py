import flet as ft
import flet_notifications as ftn

SUPPORTED = {
    ft.PagePlatform.ANDROID,
    ft.PagePlatform.ANDROID_TV,
    ft.PagePlatform.IOS,
    ft.PagePlatform.MACOS,
    ft.PagePlatform.WINDOWS,
}
MESSAGES = {2: "Ada: Lunch?", 3: "Grace: Slides attached", 4: "Alan: Ping"}


async def main(page: ft.Page):
    if not page.web and page.platform not in SUPPORTED:
        page.add(
            ft.SafeArea(
                content=ft.Text(
                    "Listing shown notifications isn't available on this platform."
                )
            )
        )
        return

    notifications = ftn.Notifications()

    def in_inbox(summary: bool = False) -> ftn.NotificationOptions:
        # Android groups by key under a summary; Apple platforms by thread.
        return ftn.NotificationOptions(
            android=ftn.AndroidOptions(
                group=ftn.AndroidGroup(key="inbox", summary=summary)
            ),
            ios=ftn.DarwinOptions(thread_identifier="inbox"),
            macos=ftn.DarwinOptions(thread_identifier="inbox"),
        )

    async def refresh():
        shown = await notifications.get_active_notifications()
        listed.controls = [
            ft.Row(
                [
                    ft.Text(f"#{n.id} {n.title or ''}"),
                    ft.TextButton(
                        "Dismiss",
                        data=n,
                        on_click=dismiss,
                    ),
                ]
            )
            for n in shown
        ] or [ft.Text("Nothing shown.")]
        page.update()

    async def post(e: ft.Event[ft.Button]):
        await notifications.request_permissions()
        for id, text in MESSAGES.items():
            await notifications.show(id, title=text, options=in_inbox())
        await notifications.show(
            1, title="3 new messages", options=in_inbox(summary=True)
        )
        await refresh()

    async def dismiss(e: ft.Event[ft.TextButton]):
        shown: ftn.ActiveNotification = e.control.data
        await notifications.cancel(shown.id, tag=shown.tag)
        await refresh()

    async def dismiss_all(e: ft.Event[ft.Button]):
        await notifications.cancel_all()
        await refresh()

    async def handle_lifecycle(e: ft.AppLifecycleStateChangeEvent):
        # Notifications may have been dismissed in the meantime.
        if e.state == ft.AppLifecycleState.RESUME:
            await refresh()

    page.on_app_lifecycle_state_change = handle_lifecycle
    listed = ft.Column()
    page.add(
        ft.SafeArea(
            content=ft.Column(
                [
                    ft.Text(
                        "Windows lists and removes notifications only for apps "
                        "packaged as MSIX.",
                        visible=not page.web
                        and page.platform == ft.PagePlatform.WINDOWS,
                    ),
                    ft.Button("Post messages", on_click=post),
                    ft.Button("Dismiss all", on_click=dismiss_all),
                    ft.Text("Shown", weight=ft.FontWeight.BOLD),
                    listed,
                ]
            )
        )
    )
    await refresh()


if __name__ == "__main__":
    ft.run(main)
