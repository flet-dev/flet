import asyncio

import flet as ft


async def main(page: ft.Page):
    def handle_switch_change(e: ft.Event[ft.Switch]):
        lv.auto_scroll = not lv.auto_scroll
        lv.update()

    lv = ft.ListView(
        spacing=10,
        padding=20,
        width=150,
        auto_scroll=True,
        controls=[
            ft.Text(f"Line {i}", color=ft.Colors.ON_SECONDARY) for i in range(0, 60)
        ],
    )

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Row(
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                    ft.Container(
                        bgcolor=ft.Colors.GREY_500,
                        content=lv,
                    ),
                    ft.Switch(
                        thumb_icon=ft.Icons.LIST_OUTLINED,
                        value=True,
                        label="Auto-scroll",
                        label_position=ft.LabelPosition.RIGHT,
                        on_change=handle_switch_change,
                    ),
                ],
            ),
        )
    )

    # Add a new item to the ListView every second.
    for i in range(len(lv.controls), 120):
        await asyncio.sleep(1)
        lv.controls.append(ft.Text(f"Line {i}", color=ft.Colors.ON_SECONDARY))
        lv.update()


if __name__ == "__main__":
    ft.run(main)
