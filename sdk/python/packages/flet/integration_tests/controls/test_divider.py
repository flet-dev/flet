import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_divider_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Divider(),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_divider_properties(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Divider(
            color=ft.Colors.RED,
            height=50,
            thickness=2,
            leading_indent=20,
            trailing_indent=20,
        ),
    )
