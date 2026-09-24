import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.FilledButton("Click me"),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_icon_only(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Row(
            controls=[
                ft.FilledButton(icon=ft.Icons.PAUSE),
                ft.FilledButton(icon=ft.Icons.PAUSE, icon_color=ft.Colors.RED),
            ],
        ),
    )
