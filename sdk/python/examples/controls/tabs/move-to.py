import random

import flet as ft


def main(page: ft.Page):
    async def handle_move_to_random(e: ft.Event[ft.FloatingActionButton]):
        # random index, excluding the current one
        i = random.choice([i for i in range(tabs.length) if i != tabs.selected_index])

        await tabs.move_to_async(
            index=i,
            animation_curve=ft.AnimationCurve.FAST_OUT_SLOWIN,
            animation_duration=ft.Duration(seconds=3),
        )

    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.MOVE_UP,
        content="Move to a random tab",
        on_click=handle_move_to_random,
    )

    page.add(
        tabs := ft.Tabs(
            length=6,
            selected_index=5,
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tab_alignment=ft.TabAlignment.CENTER,
                        tabs=[
                            ft.Tab(label=ft.Text("Tab 1")),
                            ft.Tab(label=ft.Text("Tab 2")),
                            ft.Tab(label=ft.Text("Tab 3")),
                            ft.Tab(label=ft.Text("Tab 4")),
                            ft.Tab(label=ft.Text("Tab 5")),
                            ft.Tab(label=ft.Text("Tab 6")),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Text("Tab 1 content"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("Tab 2 content"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("Tab 3 content"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("Tab 4 content"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("Tab 5 content"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("Tab 6 content"),
                                alignment=ft.Alignment.CENTER,
                            ),
                        ],
                    ),
                ],
            ),
        )
    )


ft.run(main)
