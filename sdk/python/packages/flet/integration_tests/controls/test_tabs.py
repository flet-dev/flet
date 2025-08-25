import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        name=request.node.name,
        expand_screenshot=True,
        control=ft.Tabs(
            length=2,
            content=ft.Column(
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Tab 1"),
                            ft.Tab(label="Tab 2", icon=ft.Icons.SETTINGS),
                        ]
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Container(
                                content=ft.Text("This is Tab 1"),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Container(
                                content=ft.Text("This is Tab 3"),
                                alignment=ft.Alignment.CENTER,
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_nesting(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        name=request.node.name,
        expand_screenshot=True,
        control=ft.Tabs(
            length=2,
            expand=True,
            selected_index=1,
            content=ft.Column(
                expand=True,
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label=ft.Text("Main Tab 1")),
                            ft.Tab(label=ft.Text("Main Tab 2")),
                        ],
                    ),
                    ft.TabBarView(
                        expand=True,
                        controls=[
                            ft.Text("Main Tab 1 content"),
                            ft.Tabs(
                                length=2,
                                expand=True,
                                content=ft.Column(
                                    expand=True,
                                    controls=[
                                        ft.TabBar(
                                            secondary=True,
                                            tabs=[
                                                ft.Tab(label=ft.Text("SubTab 1")),
                                                ft.Tab(label=ft.Text("SubTab 2")),
                                            ],
                                        ),
                                        ft.TabBarView(
                                            expand=True,
                                            controls=[
                                                ft.Text("Nested Tab 1 content"),
                                                ft.Text("Nested Tab 2 content"),
                                            ],
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ],
            ),
        ),
    )
