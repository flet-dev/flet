import flet as ft
import flet_notifications as ftn


def main(page: ft.Page):
    async def on_tap(e):
        print("tapped:", e.payload)

    notifications = ftn.Notifications(on_tap=on_tap)

    async def notify(e):
        if await notifications.request_permissions():
            await notifications.show(
                id=1,
                title="Build finished",
                body="Android #42 succeeded",
            )

    page.add(ft.SafeArea(content=ft.OutlinedButton(content="Notify", on_click=notify)))


if __name__ == "__main__":
    ft.run(main)
