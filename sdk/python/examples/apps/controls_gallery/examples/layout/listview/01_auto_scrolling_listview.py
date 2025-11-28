import asyncio

import flet as ft

name = "Auto-scrolling ListView"


def example():
    async def auto_scroll(e):
        count = 1
        for i in range(0, 60):
            await asyncio.sleep(1)
            lv.controls.append(ft.Text(f"Line {count}"))
            count += 1
            lv.update()

    lv = ft.ListView(spacing=10, padding=20, auto_scroll=True, height=300)

    count = 1

    for i in range(0, 60):
        lv.controls.append(ft.Text(f"Line {count}"))
        count += 1

    return ft.Column(
        controls=[
            lv,
            ft.OutlinedButton(text="Start auto-scrolling", on_click=auto_scroll),
        ]
    )
