import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.GridView(
            controls=[
                ft.Container(ft.Text("Item 1"), bgcolor=ft.Colors.BLUE),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_max_extent(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.GridView(
            max_extent=200,
            controls=[
                ft.Container(ft.Text("Item 1"), bgcolor=ft.Colors.BLUE),
                ft.Container(ft.Text("Item 2"), bgcolor=ft.Colors.GREEN),
                ft.Container(ft.Text("Item 3"), bgcolor=ft.Colors.RED),
                ft.Container(ft.Text("Item 4"), bgcolor=ft.Colors.YELLOW),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_horizontal_unbound(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.GridView(
            horizontal=True,
            controls=[
                ft.Container(
                    ft.Text("Item 1"),
                    bgcolor=ft.Colors.BLUE,
                )
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_horizontal(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.GridView(
            horizontal=True,
            height=100,
            controls=[
                ft.Container(
                    ft.Text("Item 1"),
                    bgcolor=ft.Colors.BLUE,
                ),
                ft.Container(
                    ft.Text("Item 2"),
                    bgcolor=ft.Colors.RED,
                ),
                ft.Container(
                    ft.Text("Item 3"),
                    bgcolor=ft.Colors.GREEN,
                ),
            ],
        ),
    )
