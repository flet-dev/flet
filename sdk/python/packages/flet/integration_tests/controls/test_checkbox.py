import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic_checkbox(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Checkbox(),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_checkbox_theme(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    flet_app.page.theme = ft.Theme(
        checkbox_theme=ft.CheckboxTheme(check_color=ft.Colors.RED)
    )
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Checkbox(value=True),
    )
