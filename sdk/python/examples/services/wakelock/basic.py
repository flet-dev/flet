import flet as ft


async def main(page: ft.Page):
    wakelock = ft.Wakelock()

    status = ft.Text()

    async def update_status():
        enabled = await wakelock.is_enabled()
        status.value = f"Wakelock enabled: {enabled}"

    async def enable_lock():
        await wakelock.enable()
        await update_status()

    async def disable_lock():
        await wakelock.disable()
        await update_status()

    await update_status()

    page.add(
        ft.Column(
            [
                status,
                ft.Row(
                    [
                        ft.Button("Enable wakelock", on_click=enable_lock),
                        ft.Button("Disable wakelock", on_click=disable_lock),
                    ],
                    wrap=True,
                ),
            ],
        )
    )


ft.run(main)
