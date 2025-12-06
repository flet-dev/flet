import flet as ft


async def main(page: ft.Page):
    connectivity = ft.Connectivity()

    status = ft.Text()
    changes = ft.Text()

    async def refresh(_=None):
        results = await connectivity.get_connectivity()
        status.value = "Current connectivity: " + ", ".join(r.value for r in results)

    async def on_change(e: ft.ConnectivityChangeEvent):
        changes.value = "Connectivity changed: " + ", ".join(
            r.value for r in e.connectivity
        )
        await refresh()

    connectivity.on_change = on_change

    await refresh()

    page.add(
        ft.Column(
            [
                status,
                ft.Button("Refresh connectivity", on_click=refresh),
                changes,
            ],
        )
    )


ft.run(main)
