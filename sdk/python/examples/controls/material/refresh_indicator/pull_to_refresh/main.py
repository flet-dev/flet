import asyncio
from datetime import datetime

import flet as ft


def main(page: ft.Page):
    async def handle_refresh(e: ft.Event[ft.RefreshIndicator]):
        # The indicator spins until this handler returns.
        await asyncio.sleep(1.5)
        messages.controls.insert(
            0,
            ft.ListTile(
                title=ft.Text(f"Message {len(messages.controls) + 1}"),
                subtitle=ft.Text(f"Received at {datetime.now():%H:%M:%S}"),
            ),
        )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.RefreshIndicator(
                expand=True,
                on_refresh=handle_refresh,
                content=(
                    messages := ft.ListView(
                        expand=True,
                        controls=[
                            ft.ListTile(title=ft.Text(f"Message {i}"))
                            for i in range(3, 0, -1)
                        ],
                    )
                ),
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
