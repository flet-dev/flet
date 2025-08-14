import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_elevated_button_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.ElevatedButton("Click me"),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_issue_5538(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            controls=[
                ft.ElevatedButton(
                    content="Button 1",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
                ),
                ft.ElevatedButton(
                    content="Button 2",
                    bgcolor=ft.Colors.RED,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
                ),
            ]
        ),
    )
