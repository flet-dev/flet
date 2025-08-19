import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_margin_around(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Button(
            "Button with margin",
            margin=ft.Margin.all(20),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_margin_bottom_right(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Button(
            "Button with margin",
            margin=ft.Margin.only(bottom=20, right=20),
        ),
    )
