"""Images for the Fluent overview page (index.md); each matches a snippet there."""

import flet_fluent_ui as fluent
import pytest

import flet as ft
import flet.testing as ftt


@pytest.mark.asyncio(loop_scope="function")
async def test_usage(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=fluent.FilledButton("Continue"),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_theming(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=fluent.Theme(
            accent_color=ft.Colors.PURPLE,
            content=ft.Column(
                intrinsic_width=True,
                controls=[
                    fluent.FilledButton("Save"),
                    fluent.ToggleSwitch(label="Notify me", value=True),
                ],
            ),
        ),
    )


@pytest.mark.asyncio(loop_scope="function")
async def test_icons(flet_app_function: ftt.FletTestApp, request):
    flet_app_function.page.theme_mode = ft.ThemeMode.LIGHT
    await flet_app_function.assert_control_screenshot(
        request.node.name,
        bgcolor=ft.Colors.SURFACE,
        control=ft.Row(
            tight=True,
            controls=[
                ft.Icon(fluent.FluentIcons.HOME),
                ft.Icon(fluent.FluentIcons.ALERT, color=ft.Colors.AMBER),
                ft.IconButton(fluent.FluentIcons.SETTINGS),
                fluent.IconButton(fluent.FluentIcons.HEART),
            ],
        ),
    )
