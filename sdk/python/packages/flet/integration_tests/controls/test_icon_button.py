import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_icon_button(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        control=ft.IconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_icon_button(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        control=ft.FilledIconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_tonal_icon_button(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        control=ft.FilledTonalIconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_outlined_icon_button(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        control=ft.OutlinedIconButton(ft.Icons.HOME),
    )
