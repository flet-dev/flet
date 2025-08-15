import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_list_tile_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ListTile("List Tile"),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_list_tile_properties1(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ListTile(
            "List Tile",
            subtitle="Subtitle",
            leading=ft.Icon(ft.Icons.STAR),
            trailing=ft.Icon(ft.Icons.ARROW_FORWARD),
            bgcolor=ft.Colors.LIGHT_BLUE_ACCENT_100,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
    )
