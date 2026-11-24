import asyncio
import random

import flet as ft


def get_price_tiles() -> list[ft.Control]:
    return [
        ft.ListTile(
            title=symbol,
            trailing=ft.Text(f"{random.uniform(50, 500):.2f}"),
        )
        for symbol in ["AAPL", "GOOG", "MSFT", "AMZN"]
    ]


def main(page: ft.Page):
    async def handle_refresh(e: ft.Event[ft.RefreshIndicator]):
        await asyncio.sleep(1)
        prices.controls = get_price_tiles()

    async def refresh(e: ft.Event[ft.IconButton]):
        # Pulling is a touch gesture; on desktop and web, refresh from a button.
        await indicator.show()

    page.appbar = ft.AppBar(
        title="Prices",
        actions=[
            ft.IconButton(ft.Icons.REFRESH, tooltip="Refresh", on_click=refresh),
        ],
    )
    page.add(
        ft.SafeArea(
            expand=True,
            content=(
                indicator := ft.RefreshIndicator(
                    expand=True,
                    color=ft.Colors.WHITE,
                    bgcolor=ft.Colors.BLUE,
                    on_refresh=handle_refresh,
                    content=(prices := ft.ListView(controls=get_price_tiles())),
                )
            ),
        )
    )


if __name__ == "__main__":
    ft.run(main)
