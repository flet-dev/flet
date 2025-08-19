import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_tabs_basic(flet_app: ftt.FletTestApp, request):
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
                    ft.Container(
                        expand=True,
                        content=ft.TabBarView(
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
                    ),
                ],
            ),
        ),
    )
