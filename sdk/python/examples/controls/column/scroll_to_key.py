import asyncio

import flet as ft


def main(page: ft.Page):
    page.add(
        ft.Container(
            border=ft.Border.all(1),
            content=(
                column1 := ft.Column(
                    spacing=10,
                    height=200,
                    width=300,
                    scroll=ft.ScrollMode.ALWAYS,
                    controls=[
                        ft.Container(
                            content=ft.Text("Section A", color=ft.Colors.BLACK),
                            alignment=ft.Alignment.TOP_LEFT,
                            bgcolor=ft.Colors.YELLOW_200,
                            height=100,
                            key=ft.ScrollKey("A"),
                        ),
                        ft.Container(
                            content=ft.Text("Section B", color=ft.Colors.BLACK),
                            alignment=ft.Alignment.TOP_LEFT,
                            bgcolor=ft.Colors.GREEN_200,
                            height=100,
                            key=ft.ScrollKey("B"),
                        ),
                        ft.Container(
                            content=ft.Text("Section C", color=ft.Colors.BLACK),
                            alignment=ft.Alignment.TOP_LEFT,
                            bgcolor=ft.Colors.BLUE_200,
                            height=100,
                            key=ft.ScrollKey("C"),
                        ),
                        ft.Container(
                            content=ft.Text("Section D", color=ft.Colors.BLACK),
                            alignment=ft.Alignment.TOP_LEFT,
                            bgcolor=ft.Colors.PINK_200,
                            height=100,
                            key=ft.ScrollKey("D"),
                        ),
                    ],
                )
            ),
        ),
        ft.Column(
            controls=[
                ft.Text("Scroll to:"),
                ft.Row(
                    controls=[
                        ft.ElevatedButton(
                            content="Section A",
                            on_click=lambda _: asyncio.create_task(
                                column1.scroll_to(
                                    scroll_key=ft.ScrollKey("A"), duration=1000
                                ),
                            ),
                        ),
                        ft.ElevatedButton(
                            content="Section B",
                            on_click=lambda _: asyncio.create_task(
                                column1.scroll_to(
                                    scroll_key=ft.ScrollKey("B"), duration=1000
                                ),
                            ),
                        ),
                        ft.ElevatedButton(
                            content="Section C",
                            on_click=lambda _: asyncio.create_task(
                                column1.scroll_to(
                                    scroll_key=ft.ScrollKey("C"), duration=1000
                                ),
                            ),
                        ),
                        ft.ElevatedButton(
                            content="Section D",
                            on_click=lambda _: asyncio.create_task(
                                column1.scroll_to(
                                    scroll_key=ft.ScrollKey("D"), duration=1000
                                ),
                            ),
                        ),
                    ]
                ),
            ]
        ),
    )


ft.run(main)
