import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_standard(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.IconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledIconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_filled_tonal(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledTonalIconButton(ft.Icons.HOME),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_outlined(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.OutlinedIconButton(ft.Icons.HOME),
    )
