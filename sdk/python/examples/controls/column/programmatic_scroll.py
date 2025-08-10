import flet as ft


def main(page: ft.Page):
    column = ft.Column(
        spacing=10,
        height=200,
        width=float("inf"),
        scroll=ft.ScrollMode.ALWAYS,
        controls=[
            ft.Text(f"Text line {i}", key=ft.ScrollKey(i)) for i in range(0, 100)
        ],
    )

    async def scroll_to_offset(e):
        await column.scroll_to_async(offset=500, duration=1000)

    async def scroll_to_start(e):
        await column.scroll_to_async(offset=0, duration=1000)

    async def scroll_to_end(e):
        await column.scroll_to_async(
            offset=-1, duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT
        )

    async def scroll_to_key(e):
        await column.scroll_to_async(scroll_key="20", duration=1000)

    async def scroll_to_delta(e):
        await column.scroll_to_async(delta=100, duration=200)

    async def scroll_to_minus_delta(e):
        await column.scroll_to_async(delta=-100, duration=200)

    page.add(
        ft.Container(content=column, border=ft.Border.all(1)),
        ft.ElevatedButton("Scroll to offset 500", on_click=scroll_to_offset),
        ft.Row(
            controls=[
                ft.ElevatedButton("Scroll -100", on_click=scroll_to_minus_delta),
                ft.ElevatedButton("Scroll +100", on_click=scroll_to_delta),
            ]
        ),
        ft.ElevatedButton("Scroll to key '20'", on_click=scroll_to_key),
        ft.Row(
            controls=[
                ft.ElevatedButton("Scroll to start", on_click=scroll_to_start),
                ft.ElevatedButton("Scroll to end", on_click=scroll_to_end),
            ]
        ),
    )


ft.run(main)
