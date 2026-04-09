import asyncio

import flet as ft


@ft.component
def App():
    items, set_items = ft.use_state(list(range(60)))

    async def auto_scroll(e):
        for i in range(60, 120):
            await asyncio.sleep(1)
            set_items(lambda cur, i=i: cur + [i])
            print(f"Scrolling to line {i}")

    return ft.SafeArea(
        content=ft.Column(
            controls=[
                ft.ListView(
                    spacing=10,
                    padding=20,
                    auto_scroll=True,
                    height=300,
                    controls=[
                        ft.Text(
                            key=i,
                            value=f"Line {i + 1}",
                        )
                        for i in items
                    ],
                ),
                ft.OutlinedButton("Start auto-scrolling", on_click=auto_scroll),
            ]
        )
    )


def main(page: ft.Page):
    page.render(App)


if __name__ == "__main__":
    ft.run(main)
