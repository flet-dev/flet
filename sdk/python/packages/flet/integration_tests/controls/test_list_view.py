import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_list_view_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ListView(
            controls=[
                ft.ListTile("List Tile"),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_list_view_horizontal(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ListView(
            horizontal=True,
            height=100,
            controls=[
                ft.Text("List item 1"),
                ft.Text("List item 2"),
                ft.Text("List item 3"),
            ],
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_list_view_horizontal_unbound(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ListView(
            horizontal=True,
            controls=[
                ft.Text("List item 1"),
                ft.Text("List item 2"),
                ft.Text("List item 3"),
            ],
        ),
    )
