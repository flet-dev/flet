import asyncio

import flet as ft


async def main(page: ft.Page):
    page.title = "Tabs Example"

    page.add(
        t := ft.Tabs(
            selected_index=1,
            animation_duration=300,
            expand=1,
            tabs=[
                ft.Tab(
                    label="Tab 1",
                    content=ft.Container(
                        content=ft.Text("This is Tab 1"), alignment=ft.Alignment.CENTER
                    ),
                ),
                ft.Tab(
                    label=ft.Icon(ft.Icons.MESSAGE),
                    content=ft.Text("This is Tab 2"),
                ),
                ft.Tab(
                    label="Tab 3",
                    icon=ft.Icons.IRON,
                    content=ft.Text("This is Tab 3"),
                ),
            ],
        )
    )

    await asyncio.sleep(7)
    t.selected_index = 2
    page.update()

    await asyncio.sleep(3)
    t.selected_index = 0
    page.update()

    await asyncio.sleep(3)
    t.selected_index = 1
    t.tabs.pop(0)
    t.tabs[1].content = ft.Text("Blah blah blah")
    page.update()

    await asyncio.sleep(3)
    t.tabs.clear()
    page.update()

    await asyncio.sleep(3)
    t.tabs.append(
        ft.Tab(
            label="Tab 4",
            icon=ft.Icons.LOCK,
            content=ft.Text("This is Tab 4"),
        )
    )
    t.tabs.append(
        ft.Tab(
            label="Tab 5",
            icon=ft.Icons.SIP_SHARP,
            content=ft.Text("This is Tab 5"),
        )
    )
    page.update()


ft.run(main)
