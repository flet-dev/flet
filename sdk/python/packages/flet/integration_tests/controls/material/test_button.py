import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="module")
async def test_image_for_docs(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            [
                ft.Button(content="Enabled button"),
                ft.Button(content="Disabled button", disabled=True),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_basic(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Button("Click me"),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_issue_5538(flet_app: ftt.FletTestApp, request):
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Column(
            controls=[
                ft.Button(
                    content="Button 1",
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
                ),
                ft.Button(
                    content="Button 2",
                    bgcolor=ft.Colors.RED,
                    style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=4)),
                ),
            ]
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_button_style(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Button(
            content="Test Button",
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE,
                shape=ft.RoundedRectangleBorder(radius=10),
                side=ft.BorderSide(width=3, color=ft.Colors.YELLOW),
                padding=ft.Padding.all(20),
                text_style=ft.TextStyle(
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.WHITE,
                ),
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="module")
async def test_button_style_conflicts(flet_app: ftt.FletTestApp, request):
    flet_app.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app.assert_control_screenshot(
        request.node.name,
        ft.Button(
            content="Test Button",
            elevation=10,
            color=ft.Colors.BLACK,
            bgcolor=ft.Colors.BLUE,
            style=ft.ButtonStyle(
                elevation=2,
                color=ft.Colors.WHITE,
                bgcolor=ft.Colors.RED,
            ),
        ),
    )
